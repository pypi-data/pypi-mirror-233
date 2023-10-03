from datetime import datetime
import logging
import os
from tempfile import NamedTemporaryFile
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont
import tator
from tator.openapi.tator_openapi import CreateResponse, TatorApi

from hms_import.util import (
    VESSEL_NAME_MAP,
    build_section_name,
    list_b3_files,
    list_o2_files,
    section_from_tus,
)


logger = logging.getLogger(__name__)
FONT = os.path.join(os.path.dirname(__file__), "Cascadia.ttf")
FONT_SIZE = 36
SUMMARY_IMG_SZ = 1024


def create_summary_image(
    tator_api: TatorApi,
    media_type: int,
    directory: str,
    import_type: str,
    skip_decrypt: bool = False,
    hdd_sn: Optional[str] = None,
) -> Tuple[Optional[int], str, str]:
    """Creates a summary image for a trip.

    :tator_api: The TatorApi object to use for interactions with Tator
    :media_type: The Tator media type to create
    :directory: The directory containing files to use to determine the vessel name
    :skip_decrypt: If true, use the decrypted filename format to find the vessel name
    :hdd_sn: The value for the HDD Serial Number attribute
    :returns: The created image id, section name, and found vessel name
    """

    vessel_name = "UNKNOWN"
    if import_type == "O2":
        # Get the vessel name and trip id from the first filename found starting with `stream-`
        video_list = list_o2_files(directory, skip_decrypt)
        filename = video_list[0]
        if skip_decrypt:
            name_parts = os.path.splitext(os.path.basename(filename))[0].split("-")
            vessel_name = name_parts[0]
        else:
            name_parts = os.path.splitext(os.path.basename(filename))[0].split("-")
            vessel_name = name_parts[1]
    elif import_type == "B3":
        video_list = list_b3_files(directory)
        video_path = video_list[0]
        filename = os.path.basename(video_path)
        filename_parts = os.path.splitext(os.path.basename(filename))[0].split("-")
        if len(filename_parts) == 4:
            try:
                vessel_name = filename_parts[0]
            except Exception:
                logger.warning("Could not get the vessel or section name", exc_info=True)
    else:
        raise RuntimeError(f"Received unexepected import type argument: {import_type}")

    vessel_name = VESSEL_NAME_MAP.get(vessel_name, vessel_name)
    attrs = {"Vessel Name": vessel_name}
    attrs = {
        "Vessel Name": vessel_name,
        "HDD Date Received": datetime.fromisoformat(
            datetime.today().strftime("%Y-%m-%d")
        ).isoformat(),
        "HDD Serial Number": hdd_sn,
    }

    # Check for the existence of an image with the same attributes and return that if found
    project_id = tator_api.get_media_type(media_type).project
    paginator = tator.util.get_paginator(tator_api, "get_media_list")
    page_iter = paginator.paginate(project=project_id, type=media_type)
    try:
        for page in page_iter:
            for media in page:
                attributes = getattr(media, "attributes", {})
                match = True
                for key in ["Vessel Name", "HDD Date Received", "HDD Serial Number"]:
                    if attributes.get(key, None) != attrs[key]:
                        match = False
                        break
                if match:
                    logger.info("Found existing summary image %d", media.id)
                    section = section_from_tus(
                        tator_api, project_id, media.attributes["tator_user_sections"]
                    )
                    if section:
                        section_name = section.name
                    else:
                        section_name = build_section_name(vessel_name)
                    return media.id, section_name, vessel_name
    except (RuntimeError, StopIteration):
        # Bug in paginator will raise RuntimeError if zero entities are returned
        pass

    section_name = build_section_name(vessel_name)
    label_len = max(len(key) for key in attrs.keys())
    image_text = "\n".join(f"{k: >{label_len}}: {v}" for k, v in attrs.items())
    font = ImageFont.truetype(font=FONT, size=FONT_SIZE)
    image = Image.new("RGB", (SUMMARY_IMG_SZ, SUMMARY_IMG_SZ), color="black")
    draw = ImageDraw.Draw(image)
    left, top, right, bottom = draw.textbbox((0, 0), image_text, font=font)
    x_pos = (SUMMARY_IMG_SZ - (right - left)) // 2
    y_pos = (SUMMARY_IMG_SZ - (bottom - top)) // 2
    draw.text((x_pos, y_pos), image_text, fill="white", font=font)

    with NamedTemporaryFile(suffix=".png") as temp_file:
        image.save(temp_file.name)

        import_media_args = {
            "api": tator_api,
            "type_id": media_type,
            "path": temp_file.name,
            "section": section_name,
            "fname": os.path.basename(temp_file.name),
            "attributes": {k: v for k, v in attrs.items() if v is not None},
        }

        response = None
        summary_id = None
        try:
            for progress, response in tator.util.upload_media(**import_media_args):
                logger.info("Upload progress for %s: %d%%", temp_file.name, progress)
        except Exception:
            logger.error(
                "Could not create trip summary with args:\n%s", import_media_args, exc_info=True
            )
        else:
            if isinstance(response, CreateResponse):
                logger.info("Uploaded image, received response: %s", response.message)
                summary_id = response.id

    return summary_id, section_name, vessel_name
