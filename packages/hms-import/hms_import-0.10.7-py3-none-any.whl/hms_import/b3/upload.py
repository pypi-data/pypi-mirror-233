import datetime
import logging
import os
from typing import List, Optional

import tator
from tator.openapi.tator_openapi import (
    CreateListResponse,
    File,
    FileType,
    MediaType,
    Section,
    TatorApi,
)

from hms_import import decrypt_and_transcode
from hms_import.summary_image import create_summary_image
from hms_import.util import build_section_name, list_b3_files, safe_get_type, section_from_name

logger = logging.getLogger(__name__)
DATETIME_FORMAT = "%Y%m%dT%H%M%SZ"


def create_media_objects(
    tator_api: TatorApi,
    video_list: List[str],
    media_type: MediaType,
    summary_type_id: int,
    vessel_name: str,
    section_name: str,
) -> List[int]:
    """Returns list of created or existing media ids"""
    target_ids = []
    media_type_id = media_type.id
    project_id = media_type.project
    shared_attributes = {
        "Vessel Name": vessel_name,
        "Sail Date": datetime.date.max,
        "Land Date": datetime.date.min,
    }

    # Collect media_specs
    media_specs = []
    for video_path in video_list:
        filename = os.path.basename(video_path)
        file_size = os.stat(video_path)
        if file_size == 0:
            logger.warning("Skipping media creation for empty file '%s'", filename)
            continue
        try:
            paginator = tator.util.get_paginator(tator_api, "get_media_list")
            page_iter = paginator.paginate(project=project_id, name=filename, type=media_type_id)
            try:
                media = next(media for page in page_iter for media in page)
            except (RuntimeError, StopIteration):
                # Bug in paginator will raise RuntimeError if zero entities are returned
                # If no media match this filename, create one
                filename_parts = os.path.splitext(filename)[0].split("-")
                start_datetime = datetime.datetime.min
                if len(filename_parts) == 4:
                    start_date, start_time = filename_parts[2:4]
                    try:
                        start_datetime = datetime.datetime.strptime(
                            f"{start_date}T{start_time}", DATETIME_FORMAT
                        ).replace(tzinfo=datetime.timezone.utc)
                    except Exception:
                        logger.warning("Could not parse datetime from filename '%s'", filename)
                vid_md5 = tator.util.md5sum(video_path)

                # Store the media spec and video path for creation
                media_specs.append(
                    (
                        video_path,
                        {
                            "attributes": {
                                "toc_start": start_datetime,
                                "decrypted_name": filename,
                            },
                            "name": filename,
                            "type": media_type_id,
                            "section": section_name,
                            "md5": vid_md5,
                        },
                    )
                )
            else:
                logger.info(
                    "Found existing media %d with same file name, skipping media creation",
                    media.id,
                )
                media_specs.append((media.id, None))
                start_datetime = datetime.datetime.fromisoformat(media.attributes["toc_start"])
            if start_datetime != datetime.datetime.min:
                start_date = start_datetime.date()
                shared_attributes["Sail Date"] = min(shared_attributes["Sail Date"], start_date)
                shared_attributes["Land Date"] = max(shared_attributes["Land Date"], start_date)
        except Exception:
            logger.warning("Encountered exception while processing '%s', skipping", video_path)

    # Rename section
    section = section_from_name(tator_api, project_id, section_name)
    new_section_name = section_name
    section_id = -1
    if isinstance(section, Section):
        section_id = section.id
        new_section_name = build_section_name(
            vessel_name=shared_attributes["Vessel Name"],
            sail_date=shared_attributes["Sail Date"],
            land_date=shared_attributes["Land Date"],
        )
        try:
            response = tator_api.update_section(
                section.id, section_update={"name": new_section_name}
            )
        except Exception:
            new_section_name = section_name

    # Create media objects
    for video_path_or_id, media_spec in media_specs:
        if media_spec is None:
            # Media already exists, skip
            target_ids.append(video_path_or_id)
            continue
        try:
            media_spec["section"] = new_section_name
            media_spec["attributes"].update(shared_attributes)
            response = tator_api.create_media_list(project_id, body=[media_spec])
            if isinstance(response, CreateListResponse) and response.id:
                target_ids.append(response.id[0])
        except Exception:
            logger.warning(
                "Encountered exception while processing '%s', skipping", video_path_or_id
            )

    # Update summary image, if any, with shared attributes
    shared_attributes.pop("related_files", None)
    try:
        tator_api.update_media_list(
            project_id,
            media_bulk_update={"attributes": shared_attributes},
            type=summary_type_id,
            section=section_id,
        )
    except Exception:
        logger.warning("Failed to update summary image with attributes %s", shared_attributes)

    return target_ids


def upload_sensor_data(
    tator_api: TatorApi,
    sensor_list: List[str],
    file_type: FileType,
) -> List[File]:
    file_type_id = file_type.id
    file_list = []
    for sensor_path in sensor_list:
        filename = os.path.basename(sensor_path)
        try:
            response = None
            for p, response in tator.util.upload_generic_file(
                api=tator_api,
                file_type=file_type_id,
                path=sensor_path,
                description="Raw sensor data",
                name=filename,
                timeout=120,
            ):
                logger.info("Progress for %s: %0.1f%%", filename, p)
        except Exception:
            logger.warning("Encountered exception while processing '%s', skipping", sensor_path)
            continue
        if isinstance(response, File):
            file_list.append(response)
    return file_list


def run_b3_upload(
    *,
    tator_api: TatorApi,
    media_type_id: int,
    file_type_id: int,
    multi_type_id: int,
    state_type_id: int,
    image_type_id: int,
    directory: str,
    hdd_sn: Optional[str] = None,
) -> Optional[int]:
    """
    :tator_api: The TatorApi object to use for interactions with Tator
    :media_type_id: The unique ID of the type of video to create
    :file_type_id: The unique ID of the type of file to create for storing GPS data
    :multi_type_id: The unique ID of the type of multiview to create
    :state_type_id: The unique ID of the type of State to create
    :image_type_id: The unique ID of the type of summary image to create
    :directory: The folder containing the files to import
    :hdd_sn: The hard drive serial number
    :returns: The summary image id
    """
    summary_id = None

    # Validate the given media and file types, abort if they do not exist or are incompatible
    media_type = safe_get_type(media_type_id, tator_api.get_media_type)
    file_type = safe_get_type(file_type_id, tator_api.get_file_type)
    if media_type is None:
        logger.error("Could not get media type %d from Tator, aborting", media_type_id)
        return summary_id
    if file_type is None:
        logger.error("Could not get file type %d from Tator, aborting", file_type_id)
        return summary_id
    if media_type.project != file_type.project:
        logger.error(
            "Received MediaType %d and FileType %d, which are from different projects, aborting",
            media_type_id,
            file_type_id,
        )
        return summary_id

    # Locate media for import and create summary image
    video_list = list_b3_files(directory)
    summary_id, section_name, vessel_name = create_summary_image(
        tator_api=tator_api,
        media_type=image_type_id,
        import_type="B3",
        directory=directory,
        hdd_sn=hdd_sn,
    )

    if video_list:
        target_ids = create_media_objects(
            tator_api, video_list, media_type, image_type_id, vessel_name, section_name
        )
    else:
        logger.error("No media found, aborting")
        return summary_id

    # Generate associated multiviews and GPS States
    decrypt_and_transcode.main(
        tator_api=tator_api,
        work_dir=directory,
        project_id=media_type.project,
        media_ids=target_ids,
        toc_extension=None,
        state_type=state_type_id,
        image_type=image_type_id,
        multi_type=multi_type_id,
        skip_download=True,
    )
    return summary_id
