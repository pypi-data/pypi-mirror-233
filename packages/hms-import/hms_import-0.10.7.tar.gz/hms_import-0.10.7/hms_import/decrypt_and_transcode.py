import argparse
import datetime
from glob import glob
import io
import logging
from math import floor, isnan
import os
import requests
import subprocess
import tempfile
from typing import Any, Dict, List, Optional, Union

import pynmea2
import tator
from tator.util._download_file import _download_file
from tator.openapi.tator_openapi import TatorApi
from tator.openapi.tator_openapi.models import File

from hms_import.util import LAND_DATE_PLACEHOLDER, SAIL_DATE_PLACEHOLDER, wait_for_thumbs

if __name__ != "__main__":
    logger = logging.getLogger(__name__)

LOG_EXT = ".log"
LOGS_TO_IGNORE = ["tracelog", "eventlog"]


def decrypt_file(data_dir: str, output_dir: str, private_key_path: Optional[str]) -> bool:
    retval = False
    if not private_key_path or not os.path.isfile(private_key_path):
        logger.error("Called decrypt_file with nonexistent private key path '%s'", private_key_path)
        return retval
    args = [
        "/scripts/FileProcessor",
        "--decrypt",
        private_key_path,
        "--verbose",
        output_dir,
        data_dir,
    ]
    try:
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
            if process.stdout is not None:
                for line in io.TextIOWrapper(process.stdout, newline=""):
                    logger.info(line.strip())
    except Exception:
        logger.warning(f"Attempt to decrypt contents of '{data_dir}' unsuccessful", exc_info=True)
    else:
        retval = True

    return retval


def attributes_from_toc(filename: str, toc_folder: str) -> Dict[str, Any]:
    toc_files = glob(os.path.join(toc_folder, "*.video-toc"))
    for toc_file in toc_files:
        with open(toc_file) as fp:
            for line in fp.readlines():
                try:
                    decrypted_filename, start_time_ms, end_time_ms = line.strip().split(",")
                except Exception:
                    logger.warning("Line in toc file %s malformed", toc_file)
                else:
                    if filename == decrypted_filename:
                        return {
                            "toc_filename": toc_file,
                            "toc_start": datetime.datetime.fromtimestamp(
                                int(start_time_ms) / 1000, tz=datetime.timezone.utc
                            ),
                            "toc_end": datetime.datetime.fromtimestamp(
                                int(end_time_ms) / 1000, tz=datetime.timezone.utc
                            ),
                            "decrypted_name": decrypted_filename,
                        }
    return {}


def decrypt_media(
    data_dir: str, output_dir: str, toc_extension: Optional[str], private_key_path: Optional[str]
) -> Dict[str, Any]:
    if not decrypt_file(data_dir, output_dir, private_key_path):
        return {}

    toc_files = glob(os.path.join(output_dir, f"*{toc_extension}"))
    if len(toc_files) != 1:
        logger.warning("Found %d toc files, expect exactly one, skipping", len(toc_files))
        return {}

    toc_filename = toc_files[0]
    with open(toc_filename) as fp:
        parts = fp.read().strip().split(",")

    if len(parts) != 3:
        logger.warning("Toc file %s malformed, skipping", toc_files)
        return {"toc_filename": toc_filename}

    decrypted_filename, start_time_ms, end_time_ms = parts

    return {
        "toc_filename": toc_filename,
        "toc_start": datetime.datetime.fromtimestamp(
            int(start_time_ms) / 1000, tz=datetime.timezone.utc
        ),
        "toc_end": datetime.datetime.fromtimestamp(
            int(end_time_ms) / 1000, tz=datetime.timezone.utc
        ),
        "decrypted_name": decrypted_filename,
    }


def convert_int(value: str) -> int:
    try:
        return int(value)
    except Exception:
        pass
    return 0


def convert_float(value: str) -> float:
    try:
        converted_float = float(value)
    except Exception:
        converted_float = 0.0
    else:
        if isnan(converted_float):
            converted_float = 0.0
    return converted_float


def convert_datetime(value: str) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(value, "%y%m%d%H%M%S%z")
    except Exception:
        pass
    return datetime.datetime.min


def _b3_line_to_attrs(line: str, verbose: Optional[bool] = True) -> Union[Dict[str, Any], None]:
    stripped_line = line.strip("\x00")
    if stripped_line:
        try:
            message = pynmea2.parse(f"$GPRMC,{stripped_line}")
            return {
                "Knots": message.spd_over_grnd,
                "Heading": message.true_course,
                "Datecode": message.datetime,
                "Position": [message.lon, message.lat],
            }
        except Exception:
            if verbose:
                logger.debug("Skipping malformed gps entry: '%s'", line)
    else:
        if verbose:
            logger.debug("Skipping empty gps entry: '%s'", line)
    return None


def _o2_line_to_attrs(line: str, verbose: Optional[bool] = True) -> Union[Dict[str, Any], None]:
    try:
        (
            date_col,
            time_col,
            latitude_col,
            longitude_col,
            satellite_error_col,
            speed_col,
            heading_col,
            video_col,
            pressure1_col,
            set_rotation1_col,
            retrieval_rotation1_col,
            _,
        ) = line.split(",")
    except ValueError:
        if verbose:
            logger.debug(
                "Could not split line '%s' 12 times as desired, skipping", line, exc_info=True
            )
        return None
    return {
        "Satellite Count": convert_int(satellite_error_col),
        "Knots": convert_float(speed_col),
        "Heading": convert_float(heading_col),
        "Datecode": convert_datetime(f"{date_col}{time_col}Z"),
        "Position": [convert_float(longitude_col), convert_float(latitude_col)],
        "Video": convert_int(video_col),
        "Pressure 1": convert_float(pressure1_col),
        "Set Rotation 1": convert_float(set_rotation1_col),
        "Retrieval Rotation 1": convert_float(retrieval_rotation1_col),
    }


def decrypt_metadata(
    data_dir: str, output_dir: str, private_key_path: Optional[str]
) -> Optional[str]:
    # Decrypt the file
    gps_file_path = None
    if not decrypt_file(data_dir, output_dir, private_key_path):
        return gps_file_path

    # Make sure there is exactly one file with the desired extension
    gps_list = glob(os.path.join(output_dir, f"*{LOG_EXT}"))
    if len(gps_list) == 1:
        gps_file_path = gps_list[0]
    return gps_file_path


def parse_metadata(gps_file_path: str) -> List[Dict[str, Any]]:
    # Convert the lines of the file to attributes
    with open(gps_file_path) as fp:
        lines = fp.readlines()

    # Determine which style of gps file this by finding the first parsable line
    parser = None
    for line in lines:
        if _b3_line_to_attrs(line, verbose=False):
            parser = _b3_line_to_attrs
            break
        if _o2_line_to_attrs(line, verbose=False):
            parser = _o2_line_to_attrs
            break

    metadata = []
    if parser:
        logger.debug("Using parser %s", parser.__name__)
        metadata = [parser(line) for line in lines]

    return [point for point in metadata if point]


def parse_and_upload(
    tator_api: TatorApi, log_filename: str, summary_image_id: Optional[int]
) -> List:
    data = []
    if any(kw in log_filename for kw in LOGS_TO_IGNORE):
        logger.debug("Not parsing log file '%s'; it does not contain GPS data", log_filename)
    else:
        data.extend(parse_metadata(log_filename))
    if os.path.isfile(log_filename) and os.stat(log_filename).st_size:
        try:
            for _ in tator.util.upload_attachment(
                api=tator_api, media=summary_image_id, path=log_filename
            ):
                pass
        except Exception:
            pass
    return data


def main(
    *,
    tator_api: TatorApi,
    work_dir: str,
    project_id: int,
    media_ids: List[int],
    toc_extension: Optional[str],
    state_type: int,
    image_type: int,
    multi_type: int,
    private_key_path: Optional[str] = None,
    skip_download: Optional[bool] = False,
) -> Optional[int]:
    media_list = tator_api.get_media_list_by_id(project_id, media_id_query={"ids": media_ids})
    section_name = ""
    section_id = -1
    media_type_id = None
    media_type = None
    summary_image_id = None
    if media_list:
        media = media_list[0]
        media_type_id = media.type
        media_type = tator_api.get_media_type(media_type_id)
        tator_user_sections = media.attributes["tator_user_sections"]
        section_list = tator_api.get_section_list(project_id)
        if isinstance(section_list, list):
            for sec in section_list:
                if sec.tator_user_sections == tator_user_sections:
                    section_name = sec.name
                    section_id = sec.id
                    break

    image_list = tator_api.get_media_list(project_id, section=section_id, type=image_type)
    if image_list:
        summary_image_id = image_list[0].id

    desired_streaming_resolutions = set()
    if hasattr(media_type, "streaming_config") and media_type.streaming_config:
        desired_streaming_resolutions.update(
            [config.resolution for config in media_type.streaming_config]
        )
    datetime_lookup = {}
    starts_and_ids = []

    # Decrypt and transcode all media files first
    logger.info("Importing media")
    sail_date = datetime.date.max
    land_date = datetime.date.min
    vessel_name = None
    for media in media_list:
        # Idempotency check to determine if a file needs to be downloaded and decrypted
        attributes = {}
        needs_transcode = True
        if (
            hasattr(media, "media_files")
            and media.media_files
            and hasattr(media.media_files, "streaming")
            and media.media_files.streaming
        ):
            needs_transcode = False
            for attr, converter in [
                ("toc_start", datetime.datetime.fromisoformat),
                ("decrypted_name", str),
            ]:
                if attr in getattr(media, "attributes", {}):
                    attributes[attr] = converter(media.attributes[attr])
                else:
                    needs_transcode = True

            if not needs_transcode:
                extant_resolutions = set(
                    [config.resolution[0] for config in media.media_files.streaming]
                )
                if extant_resolutions != desired_streaming_resolutions:
                    needs_transcode = True

        # Initialize with None and update with media object if `needs_transcode` is False or if
        # the decryption is successful, otherwise it will remain None and not be considered for
        # multiview generation
        updated_media = None
        transcode_response = None
        if needs_transcode:
            with tempfile.TemporaryDirectory(dir=work_dir) as data_dir, tempfile.TemporaryDirectory(
                dir=work_dir
            ) as output_dir:
                # Get download info for encrypted file
                if skip_download:
                    source_dir = work_dir
                    decrypted_name = media.attributes["decrypted_name"]
                    toc_attributes = attributes_from_toc(decrypted_name, work_dir)
                    if toc_attributes:
                        attributes = toc_attributes
                    else:
                        attributes = {
                            "toc_start": datetime.datetime.fromisoformat(
                                media.attributes["toc_start"]
                            ),
                            "decrypted_name": decrypted_name,
                        }
                        if media.attributes.get("toc_end", None):
                            attributes["toc_end"] = datetime.datetime.fromisoformat(
                                media.attributes["toc_end"]
                            )
                else:
                    encrypted_path = media.attributes["encrypted_path"]
                    download_path = os.path.join(data_dir, media.name)
                    for _ in _download_file(
                        tator_api, media.project, encrypted_path, download_path
                    ):
                        pass

                    # Decrypt and transcode the file
                    attributes = decrypt_media(
                        data_dir, output_dir, toc_extension, private_key_path
                    )
                    if not attributes:
                        logger.warning("Could not decrypt %s, skipping transcode", media.name)
                        continue

                    source_dir = output_dir

                # Upload toc file, if appropriate
                toc_filename = attributes.pop("toc_filename", None)
                if toc_filename and os.path.isfile(toc_filename):
                    try:
                        for _, response in tator.util.upload_attachment(
                            tator_api, media.id, toc_filename
                        ):
                            pass
                    except Exception:
                        logger.warning("Could not upload toc file %s", toc_filename, exc_info=True)
                    else:
                        logger.debug(
                            "Uploaded toc file %s as an attachment on media %d",
                            toc_filename,
                            media.id,
                        )

                # Update media attributes
                try:
                    tator_api.update_media(media.id, media_update={"attributes": attributes})
                except Exception:
                    logger.warning(
                        "Could not update media %d with attributes %s", media.id, attributes
                    )

                filename = attributes.get("decrypted_name", "")
                path = os.path.join(source_dir, filename)
                if filename and os.path.isfile(path):
                    if os.stat(path).st_size:
                        logger.info("Uploading media for %s", filename)
                        for p, transcode_response in tator.util.upload_media(
                            api=tator_api,
                            type_id=media.type,
                            path=path,
                            md5=tator.util.md5sum(path),
                            fname=filename,
                            media_id=media.id,
                            timeout=120,
                        ):
                            logger.info("Upload progress for %s: %0.1f%%", filename, p)
                        updated_media = media
                    else:
                        logger.warning(
                            "File '%s' is empty, skipping upload for media id %d",
                            filename,
                            media.id,
                        )
                else:
                    logger.error("Error decrypting %s", media.name)
                    err_log_path = f"{path}.log"

                    if os.path.isfile(err_log_path) and os.stat(err_log_path).st_size:
                        try:
                            for _, response in tator.util.upload_attachment(
                                tator_api, media.id, err_log_path
                            ):
                                pass
                        except Exception:
                            logger.warning(
                                "Could not upload error log file %s", err_log_path, exc_info=True
                            )
                        else:
                            logger.debug(
                                "Uploaded error log file %s as an attachment on media %d",
                                err_log_path,
                                media.id,
                            )
                        with open(err_log_path) as fp:
                            for line in fp.readlines():
                                logger.error(line.strip())
                    else:
                        logger.error("Could not open log file at '%s'", err_log_path)
        else:
            updated_media = media

        # Store info for creating multiviews
        if updated_media:
            starts_and_ids.append(
                (
                    attributes["toc_start"],
                    media.id,
                    transcode_response.id if transcode_response else None,
                )
            )
            datetime_lookup[media.id] = {"obj": updated_media, **attributes}
            start_date = attributes["toc_start"].date()
            sail_date = min(sail_date, start_date)
            land_date = max(land_date, start_date)
            if not vessel_name:
                vessel_name = media.attributes.get("Vessel Name", None)

    # Wait for thumbnail generation (and fps/num_frame counts), then update media objects
    starts_and_ids = wait_for_thumbs(tator_api, project_id, starts_and_ids)

    # Remove invalid ids from `datetime_lookup`
    remaining_ids = [item[1] for item in starts_and_ids]
    for media_id in list(datetime_lookup.keys()):
        if media_id not in remaining_ids:
            datetime_lookup.pop(media_id, None)

    # Refresh media objects
    for media in tator_api.get_media_list_by_id(
        project_id, media_id_query={"ids": list(datetime_lookup.keys())}
    ):
        datetime_lookup[media.id]["obj"] = media

    starts_and_ids.sort()
    current_start, media_id, _ = starts_and_ids[0]
    multi_lookup = {current_start: [media_id]}
    for start_dt, media_id, _ in starts_and_ids[1:]:
        if (start_dt - current_start).total_seconds() > 5:
            multi_lookup[start_dt] = []
            current_start = start_dt
        multi_lookup[current_start].append(media_id)
    # Determine extant multiviews by comparing against id lists and remove from creation list
    media_id_sets = [(start, set(media_ids)) for start, media_ids in multi_lookup.items()]
    paginator = tator.util.get_paginator(tator_api, "get_media_list")
    kwargs = {"project": project_id, "type": multi_type}
    if section_id:
        kwargs["section"] = section_id
    page_iter = paginator.paginate(**kwargs)
    try:
        for page in page_iter:
            for multi in page:
                multi_id_set = set()
                if (
                    hasattr(multi, "media_files")
                    and hasattr(multi.media_files, "ids")
                    and multi.media_files.ids
                ):
                    multi_id_set.update(multi.media_files.ids)
                if multi_id_set:
                    for start, media_id_set in media_id_sets:
                        if multi_id_set == media_id_set:
                            multi_lookup.pop(start, None)
                            break
    except RuntimeError:
        # Paginator has a bug in handling zero results
        pass

    # Create non-existent multiviews
    logger.info("Creating %d multiviews", len(multi_lookup))
    for start, media_ids in multi_lookup.items():
        # Sort media by filename for consistent display order
        media_objects = [datetime_lookup[media_id]["obj"] for media_id in media_ids]
        media_objects.sort(key=lambda ele: ele.name)
        ordered_media_ids = [m.id for m in media_objects]

        # Commented out until frame-accurate seek works with frame offsets
        # Get latest start time
        # multi_start = max(datetime_lookup[media_id]["toc_start"] for media_id in media_ids)

        # Calculate frame offsets
        # frame_offsets = [
        #     floor(
        #         (multi_start - datetime_lookup[media.id]["toc_start"]).total_seconds() * media.fps
        #     )
        #     if media.fps
        #     else 0
        #     for media in media_objects
        # ]

        try:
            tator.util.make_multi_stream(
                api=tator_api,
                type_id=multi_type,
                layout=[1, len(ordered_media_ids)],
                name=start.isoformat(),
                media_ids=ordered_media_ids,
                section=section_name,
                # frame_offset=frame_offsets,
            )
        except Exception:
            logger.warning(
                "Failed to make multi for start time %s", start.isoformat(), exc_info=True
            )

    # Update section and media with sail and land dates
    new_section_name = section_name
    new_section_name = new_section_name.replace(
        SAIL_DATE_PLACEHOLDER, sail_date.strftime("%Y-%m-%d")
    )
    new_section_name = new_section_name.replace(
        LAND_DATE_PLACEHOLDER, land_date.strftime("%Y-%m-%d")
    )
    if new_section_name != section_name:
        try:
            tator_api.update_section(section_id, section_update={"name": new_section_name})
        except Exception:
            logger.warning(
                "Could not change section name from %s to %s",
                section_name,
                new_section_name,
                exc_info=True,
            )
    bulk_update = {
        "attributes": {
            "Sail Date": sail_date,
            "Land Date": land_date,
            "Vessel Name": vessel_name,
        }
    }
    for mt in [media_type_id, multi_type, image_type]:
        try:
            tator_api.update_media_list(project_id, bulk_update, type=mt, section=section_id)
        except Exception:
            logger.warning(
                "Could not apply bulk update '%s' to MediaType %d", bulk_update, mt, exc_info=True
            )

    related_file_ids = set(
        int(file_id)
        for entry in datetime_lookup.values()
        for file_id in entry["obj"].attributes.get("related_files", "").split(",")
        if file_id.isnumeric()  # Protects against an empty string
    )

    # For idempotency, delete any existing state specs on the media, one media at a time to avoid
    # too many deletions
    for media_id in datetime_lookup.keys():
        try:
            response = tator_api.delete_state_list(project_id, media_id=[media_id])
        except Exception:
            logger.warning("Could not delete existing states on media %d", media_id, exc_info=True)

    metadata = []
    if related_file_ids:
        for file_id in related_file_ids:
            file_obj = tator_api.get_file(file_id)
            if not isinstance(file_obj, File):
                logger.warning("Could not find file with id %d, skipping", file_id)
                continue
            if not isinstance(file_obj.name, str):
                logger.warning("Could not get name of file %d, skipping", file_id)
                continue
            download_info = tator_api.get_download_info(
                file_obj.project, download_info_spec={"keys": [file_obj.path]}
            )

            if not (download_info and isinstance(download_info, list) and download_info[0].url):
                logger.warning(
                    "Could not get download info for '%s' (%d), skipping", file_obj.name, file_id
                )
                continue
            else:
                download_url = download_info[0].url

            # Make working directories
            with tempfile.TemporaryDirectory(dir=work_dir) as data_dir, tempfile.TemporaryDirectory(
                dir=work_dir
            ) as output_dir:
                # Download the encrypted GPS file
                encrypted_path = os.path.join(data_dir, file_obj.name)
                response = requests.get(download_url, stream=True)
                with open(encrypted_path, "wb") as fp:
                    for chunk in response.iter_content(chunk_size=128):
                        fp.write(chunk)

                if private_key_path:
                    log_filename = decrypt_metadata(data_dir, output_dir, private_key_path)
                else:
                    log_filename = encrypted_path
                if log_filename:
                    metadata.extend(parse_and_upload(tator_api, log_filename, summary_image_id))
    else:
        log_list = glob(os.path.join(work_dir, f"*{LOG_EXT}"))
        # Convert the lines of the file to attributes
        for log_filename in log_list:
            metadata.extend(parse_and_upload(tator_api, log_filename, summary_image_id))

    logger.info("Parsed %d points", len(metadata))
    metadata.sort(key=lambda ele: ele["Datecode"])
    state_specs = []
    # Create a state spec for each point/media pair, where the point timestamp occurs between
    # the start and stop timestamps of the media object
    for media_id, media_info in datetime_lookup.items():
        media = media_info["obj"]
        toc_start = datetime.datetime.fromisoformat(media.attributes["toc_start"])
        fps = media.fps
        if fps is None:
            logger.warning(f"Media {media_id} does not have a valid fps, no states will be created.")
            continue
        toc_end = media.attributes.get("toc_end")
        if not toc_end:
            toc_end = toc_start + datetime.timedelta(seconds=fps * media.num_frames)
        else:
            toc_end = datetime.datetime.fromisoformat(toc_end)

        # Find first and last points in the sorted list of metadata
        start_idx = 0
        for idx, point in enumerate(metadata):
            if point["Datecode"] >= toc_start:
                start_idx = idx
                break
        if start_idx >= len(metadata):
            logger.warning("Could not find a valid start index for gps data in media %d", media_id)
            continue
        stop_idx = -1
        for idx, point in enumerate(metadata[start_idx:]):
            if point["Datecode"] >= toc_end:
                stop_idx = idx + start_idx
                break
        if stop_idx >= len(metadata):
            logger.warning("Could not find a valid start index for gps data in media %d", media_id)
            continue

        state_specs.extend(
            (
                {
                    "type": state_type,
                    "media_ids": [media_id],
                    "frame": floor(
                        (point["Datecode"] - media_info["toc_start"]).total_seconds() * fps
                    ),
                    "attributes": point,
                }
                for point in metadata[start_idx:stop_idx]
            )
        )

    for response in tator.util.chunked_create(
        tator_api.create_state_list, project_id, body=state_specs
    ):
        logger.info(response.message)

    return summary_image_id


if __name__ == "__main__":
    from hms_import.util import HmsLogHandler

    parser = argparse.ArgumentParser(
        description="Script for decrypting and transcoding encrypted video files"
    )
    # Get updated media file metadata
    tator.get_parser(parser)
    parser.add_argument("--work-dir", type=str, required=True)
    parser.add_argument("--project-id", type=int, required=True)
    parser.add_argument("--media-ids", nargs="+", type=int, required=True)
    parser.add_argument("--toc-extension", type=str, required=True)
    parser.add_argument("--state-type", type=int, required=True)
    parser.add_argument("--image-type", type=int, required=True)
    parser.add_argument("--multi-type", type=int, required=True)
    parser.add_argument("--private-key-path", type=str, required=False)
    args = parser.parse_args()
    argdict = vars(args)
    host = argdict.pop("host")
    token = argdict.pop("token")
    api = tator.get_api(host=host, token=token)
    argdict["tator_api"] = api

    with HmsLogHandler(
        tator_api=api,
        console_log_level=logging.DEBUG,
        log_filename=f"{os.path.splitext(os.path.basename(__file__))[0]}.log",
    ) as log_handler:
        logger = logging.getLogger(__file__)
        log_handler.summary_image_id = main(**argdict)
