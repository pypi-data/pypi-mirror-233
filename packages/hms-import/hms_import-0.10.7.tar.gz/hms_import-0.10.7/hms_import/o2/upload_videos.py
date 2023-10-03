#!/usr/bin/env python3

import datetime
from glob import glob
import hashlib
import logging
import os
from pprint import pformat
from typing import Any, Dict, List, Optional, Tuple

import tator
from tator.openapi.tator_openapi import TatorApi
from tator.openapi.tator_openapi.models import CreateListResponse, UploadInfo
from tator.util._upload_file import _upload_file

from hms_import.util import list_o2_files


logger = logging.getLogger(__name__)


def _calculate_md5(file_path):
    hash_md5 = hashlib.md5()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def get_start_end_times(path: str) -> Tuple[datetime.datetime, datetime.datetime]:
    directory = os.path.dirname(path)
    filename = os.path.basename(path)
    logger.info(f"Searching for toc_files in {directory=}")
    toc_files = list(glob(os.path.join(directory, f"*.video-toc")))
    logger.info(f"Searching for {filename=} in {toc_files=}")
    for toc_file in toc_files:
        with open(toc_file) as fp:
            for line in fp.readlines():
                decrypted_filename, start_time_ms, end_time_ms = line.strip().split(",")
                if decrypted_filename == filename:
                    return (
                        datetime.datetime.fromtimestamp(
                            int(start_time_ms) / 1000, tz=datetime.timezone.utc
                        ),
                        datetime.datetime.fromtimestamp(
                            int(end_time_ms) / 1000, tz=datetime.timezone.utc
                        ),
                    )
    raise RuntimeError(f"Could not get start and end times for {filename}!")


def _upload_video(
    tator_api: TatorApi,
    path: str,
    project_id: int,
    media_type: int,
    file_ids: List[int],
    section: str,
    vessel_name: str,
    skip_decrypt: bool,
) -> Optional[int]:
    # Perform idempotency check
    filename = os.path.basename(path)
    paginator = tator.util.get_paginator(tator_api, "get_media_list")
    page_iter = paginator.paginate(project=project_id, name=filename, type=media_type)
    try:
        media = next(media for page in page_iter for media in page)
    except (RuntimeError, StopIteration):
        # Bug in paginator will raise RuntimeError if zero entities are returned
        pass
    else:
        logger.info(
            "Found existing media %d with same file name, skipping media creation%s",
            media.id,
            "" if skip_decrypt else " and upload",
        )
        return media.id

    # Skip empty files
    file_size = os.stat(path).st_size
    if file_size == 0:
        logger.warning("Skipping empty file '%s'", filename)
        return None

    attrs: Dict[str, Any] = {"Vessel Name": vessel_name}
    if skip_decrypt:
        toc_start, toc_end = get_start_end_times(path)
        attrs["decrypted_name"] = filename
        attrs["toc_start"] = toc_start
        attrs["toc_end"] = toc_end
    else:
        # Upload encrypted file to Tator
        logger.info("Uploading %s", filename)
        response = None
        try:
            for progress, response in _upload_file(
                tator_api, project_id, path=path, filename=filename, file_size=file_size
            ):
                logger.info("Upload progress: %.1f%%", progress)
        except Exception as exc:
            raise RuntimeError(f"Raised exception while uploading '{filename}', skipping") from exc

        if not isinstance(response, UploadInfo) or response.key is None:
            raise RuntimeError(f"Did not upload '{filename}', skipping")

        logger.info("Uploading %s successful!", filename)
        attrs["encrypted_path"] = response.key
        attrs["related_files"] = ",".join(str(file_id) for file_id in file_ids)

    # Create a media object containing the key to the uploaded file
    media_spec = {
        "type": media_type,
        "section": section,
        "name": filename,
        "md5": _calculate_md5(path),
        "attributes": attrs,
    }

    logger.info(
        "Creating media object in project %d with media_spec=%s", project_id, pformat(media_spec)
    )
    try:
        response = tator_api.create_media_list(project_id, [media_spec])
    except Exception as exc:
        raise RuntimeError(f"Could not create media with {project_id=} and {media_spec=}") from exc

    return response.id[0] if isinstance(response, CreateListResponse) and response.id else 0


def upload_videos(
    *,
    tator_api: TatorApi,
    directory: str,
    project_id: int,
    media_type: int,
    section: str,
    file_ids: List[int],
    vessel_name: str,
    skip_decrypt: bool,
) -> List[int]:
    """
    Finds all encrypted video files in `directory`, uploads them to Tator, and creates a media
    object referencing the upload. A future algorithm will be responsible for decrypting and
    transcoding them. Disallows use of positional arguments.

    :tator_api: The TatorApi object to use for interactions with Tator
    :param token: The Tator API token to use for authentication.
    :type token: str
    :param directory: The directory to search for encrypted video files.
    :type directory: str
    :param project_id: The integer id of the project to upload the videos to.
    :type project_id: int
    :param media_type: The integer id of the media type to create.
    :type media_type: int
    :param section: The section to upload the media to.
    :type section: str
    :param file_ids: The list of file ids to associate uploaded media with.
    :type file_ids: List[int]
    :param vessel_name: The dict of shared attributes for all media.
    :type vessel_name: Dict[str, str]
    :param skip_decrypt: If True, skips uploading encrypted files and assumes files in `directory`
                         are previously decrypted legacy files
    :type skip_decrypt: bool
    """
    file_list = list_o2_files(directory, skip_decrypt)
    logger.info("Found the following files:\n* %s", "\n* ".join(file_list))

    results = []
    for filename in file_list:
        try:
            media_id = _upload_video(
                tator_api,
                filename,
                project_id,
                media_type,
                file_ids,
                section,
                vessel_name,
                skip_decrypt,
            )
        except Exception:
            logger.error("Failed to upload '%s'", os.path.basename(filename), exc_info=True)
        else:
            if media_id:
                results.append(media_id)
    return results
