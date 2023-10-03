from configparser import ConfigParser
import logging
from pprint import pformat

from tator.openapi.tator_openapi import TatorApi

from hms_import import decrypt_and_transcode
from hms_import.o2.upload_metadata import upload_metadata
from hms_import.o2.upload_videos import upload_videos
from hms_import.summary_image import create_summary_image
from hms_import.util import validate_type_from_config

logger = logging.getLogger(__name__)


def run_o2_upload(tator_api: TatorApi, config: ConfigParser):
    project_id = config["Tator"].getint("ProjectId", -1)
    if project_id < 0:
        raise ValueError(f"Missing ProjectId value in the Tator section of the config file")
    try:
        tator_api.get_project(project_id)
    except Exception as exc:
        raise ValueError(f"Could not get project {project_id}") from exc

    skip_decrypt = config["Tator"].getboolean("SkipDecrypt", False)
    file_type = validate_type_from_config(tator_api, config, "FileType", project_id, "file_type")
    media_type = validate_type_from_config(
        tator_api, config, "MediaType", project_id, "media_type", list_filters=[("dtype", "video")]
    )
    summary_type = validate_type_from_config(
        tator_api,
        config,
        "SummaryType",
        project_id,
        "media_type",
        list_filters=[("dtype", "image")],
    )
    directory = config["Local"]["Directory"]

    # Create trip summary image
    create_summary_kwargs = {
        "media_type": summary_type,
        "directory": directory,
        "import_type": "O2",
        "skip_decrypt": skip_decrypt,
        "hdd_sn": config["Trip"].get("HddSerialNumber", None),
    }
    logger.info("Creating trip summary with configuration %s", pformat(create_summary_kwargs))
    summary_id, section, vessel_name = create_summary_image(tator_api, **create_summary_kwargs)
    if section:
        logger.info("Created trip summary in section %s", section)
    else:
        raise RuntimeError("Could not create trip summary and section")

    # Construct metadata argument dictionary for logging (do not log token for security)
    file_ids = []
    if skip_decrypt:
        logger.info("Skipping metadata upload for legacy format")
    else:
        upload_metadata_kwargs = {
            "project_id": project_id,
            "directory": directory,
            "file_type": file_type,
        }
        logger.info(
            "Starting metadata upload with configuration %s", pformat(upload_metadata_kwargs)
        )
        file_ids = upload_metadata(tator_api=tator_api, **upload_metadata_kwargs)
        logger.info("Metadata upload complete!")

    # Construct video argument dictionary for logging (do not log token for security)
    upload_video_kwargs = {
        "directory": directory,
        "project_id": project_id,
        "file_ids": file_ids,
        "media_type": media_type,
        "section": section,
        "vessel_name": vessel_name,
        "skip_decrypt": skip_decrypt,
    }
    logger.info("Starting video upload with configuration %s", pformat(upload_video_kwargs))
    media_ids = upload_videos(tator_api=tator_api, **upload_video_kwargs)
    logger.info("Video upload complete!")
    logger.info("Created the following media: %s", pformat(media_ids))

    if skip_decrypt:
        logger.info("Skipping decryption, starting transcodes...")
        decrypt_and_transcode.main(
            tator_api=tator_api,
            work_dir=directory,
            project_id=project_id,
            media_ids=media_ids,
            toc_extension=".video-toc",
            state_type=config["Tator"].getint("StateType"),
            image_type=summary_type,
            multi_type=config["Tator"].getint("MultiType"),
            skip_download=True,
        )
    else:
        logger.info(
            "Launching decryption workflow for %d media objects and %d metadata files",
            len(media_ids),
            len(file_ids),
        )

        # Launch one workflow for all media ids
        algorithm_name = config["Tator"]["AlgorithmName"]
        job_spec = {"algorithm_name": algorithm_name, "media_ids": media_ids}
        try:
            response = tator_api.create_job_list(project=project_id, job_spec=job_spec)
        except Exception:
            logger.error(
                "Could not launch job with job_spec=%s in project %d",
                pformat(job_spec),
                project_id,
                exc_info=True,
            )
        else:
            logger.info(
                "Launched workflow %s on media %s (received response %s)",
                algorithm_name,
                pformat(media_ids),
                pformat(response),
            )
    return summary_id
