from configparser import ConfigParser
from datetime import date, datetime
from glob import glob
from io import TextIOBase
import logging
from logging import FileHandler, StreamHandler
import os
import sys
from time import sleep
from typing import Any, Callable, List, Optional, TextIO, Tuple

from tator.openapi.tator_openapi import Section, TatorApi
from tator.util import upload_attachment

logger = logging.getLogger(__name__)

SAIL_DATE_PLACEHOLDER = "NO_SAIL_DATE"
LAND_DATE_PLACEHOLDER = "NO_LAND_DATE"
VESSEL_NAME_MAP = {
    "1022773": "Eagle Eye II",
    "1027010": "Alex Marie",
    "1029712": "Kenny Boy",
    "1031845": "Destiny",
    "1038712": "Ellen Jean",
    "1049623": "Leo B",
    "1061277": "Miss Kaleigh",
    "1075516": "Jamie B",
    "1081640": "Capt Easy",
    "1097631": "Hanna Katherine",
    "1231179": "Full Timer",
    "1231553": "Dayboat One",
    "1275363": "Market Price",
    "507646": "Daytona",
    "510728": "Miss Suzanne",
    "539456": "Bookie",
    "541694": "Eaglet II",
    "557860": "Independence",
    "579208": "Galilean",
    "591301": "Charleston Star",
    "592269": "Capt. Gorman III",
    "595941": "Blue Wave",
    "596805": "Mary Ann",
    "597797": "Bluefin",
    "600048": "Kim Thanh II",
    "600293": "4 Cs",
    "600322": "Bobalou",
    "604915": "Frances Ann",
    "608436": "Christopher Joe",
    "609121": "Carol Ann",
    "610006": "Captain Michael",
    "610080": "Blessings",
    "611243": "Erica Lynn",
    "616696": "Cynthia Renee",
    "620696": "Albi",
    "622027": "Carter Anthony",
    "624406": "Dayboat Too",
    "628300": "Bigeye",
    "630306": "Defiance",
    "633432": "Kelly Ann",
    "638863": "Miss Shannon",
    "641486": "Miss Ann",
    "646506": "Janice Ann",
    "651698": "Intrepido II",
    "652211": "Lisa Ann",
    "655108": "Miss Haylee II",
    "656259": "Kristin Lee",
    "659026": "Eyelander",
    "661098": "Miss Rita",
    "661284": "Hannah Boden",
    "662409": "Fine Tuna",
    "665962": "Linnea C",
    "668316": "Capt. Luu",
    "669872": "Eagle Eye",
    "671174": "Delphinus",
    "673556": "Candace",
    "674417": "Bear",
    "680845": "Endeavor",
    "683311": "Iron Maiden",
    "904300": "Kim Nhi",
    "905679": "Capt. Mike",
    "908045": "Julianne",
    "911431": "Capt. David",
    "912738": "Joshua Nicole",
    "913385": "2nd Wind",
    "918933": "Miss Lena",
    "919799": "Blue Sea I",
    "929813": "Capt. Bob",
    "936041": "Cecelia II",
    "937416": "Kim Thanh",
    "956008": "Dakota",
    "957958": "Miss Jane",
    "969495": "Hannah Story",
    "983321": "Blue Sea 2",
    "997091": "Alexandria Dawn",
    "FL5295PN": "Big B",
    "MD9128BD": "Integrity",
    "MS1993DD": "Angel's Grace",
    "NC2015WS": "Kaitlyn C",
    "NC3377EM": "Big Dave",
    "NC5126DC": "Hardway",
    "NC5516DF": "Fish Wish",
    "NC6362EX": "Big Skipper",
    "NC8831WR": "Body Count",
    "NJ4755FP": "Backwash",
}


def validate_type_from_config(
    api: TatorApi,
    config: ConfigParser,
    config_field: str,
    project_id: int,
    tator_type: str,
    list_filters=None,
) -> int:
    if tator_type not in ["media_type", "file_type"]:
        raise ValueError(f"Cannot validate {config_field=} for {tator_type=}")

    type_id = config["Tator"].getint(config_field, -1)
    if type_id > 0:
        try:
            getattr(api, f"get_{tator_type}")(type_id)
        except Exception as exc:
            raise ValueError(f"Could not find {config_field} with id {type_id}") from exc
    else:
        try:
            types = getattr(api, f"get_{tator_type}_list")(project_id)
        except Exception as exc:
            raise RuntimeError(f"Could not list {config_field}s from project {project_id}") from exc
        if list_filters:
            for attr, value in list_filters:
                types = [
                    _type
                    for _type in types
                    if hasattr(_type, attr) and getattr(_type, attr) == value
                ]
        if len(types) > 1:
            raise ValueError(
                f"Project {project_id} has more than one {config_field}, specify one of the "
                f"following in the config: {types}"
            )
        type_id = types[0].id
    return type_id


def safe_get_type(type_id: int, type_getter: Callable[[int], Any]):
    type_inst = None
    try:
        type_inst = type_getter(type_id)
    except Exception:
        logger.error("Could not find type %d", type_id, exc_info=True)
    return type_inst


def build_section_name(
    vessel_name: str, sail_date: Optional[date] = None, land_date: Optional[date] = None
) -> str:
    try:
        sail_date_str = sail_date.strftime("%Y-%m-%d") if sail_date else SAIL_DATE_PLACEHOLDER
    except Exception:
        sail_date_str = SAIL_DATE_PLACEHOLDER
    try:
        land_date_str = land_date.strftime("%Y-%m-%d") if land_date else LAND_DATE_PLACEHOLDER
    except Exception:
        land_date_str = LAND_DATE_PLACEHOLDER

    return f"{vessel_name} ({sail_date_str} - {land_date_str})"


def section_from_tus(
    tator_api: TatorApi, project_id: int, tator_user_sections: str
) -> Optional[Section]:
    section = None
    try:
        section_list = tator_api.get_section_list(project_id)
    except Exception:
        pass
    else:
        if isinstance(section_list, list):
            for sec in section_list:
                if sec.tator_user_sections == tator_user_sections:
                    section = sec
                    break
    return section


def section_from_name(tator_api: TatorApi, project_id: int, section_name: str) -> Optional[Section]:
    section = None
    try:
        section_list = tator_api.get_section_list(project_id)
    except Exception:
        pass
    else:
        if isinstance(section_list, list):
            for sec in section_list:
                if sec.name == section_name:
                    section = sec
                    break
    return section


class HmsLogHandler(TextIOBase):
    log_filename = os.path.join(os.getcwd(), f"{__name__.split('.')[0]}.log")

    def __init__(
        self, tator_api: TatorApi, console_log_level: int, log_filename: Optional[str] = None
    ):
        super().__init__()
        self._api: TatorApi = tator_api
        self._log_filename = log_filename or HmsLogHandler.log_filename
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        self._console_handler: StreamHandler = logging.StreamHandler()
        self._console_handler.setLevel(console_log_level)
        self._file_handler: FileHandler = FileHandler(filename=self._log_filename, mode="w")
        self._file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "[%(asctime)s - %(levelname)s - %(module)s>%(funcName)s]: %(message)s"
        )
        self._console_handler.setFormatter(formatter)
        self._file_handler.setFormatter(formatter)
        root_logger.addHandler(self._console_handler)
        root_logger.addHandler(self._file_handler)
        self._stdout: TextIO = sys.stdout
        self._stderr: TextIO = sys.stderr

        # Set the summary image id before leaving the context and HmsLogHandler will automatically
        # upload its log file as an attachment to the image
        self._summary_image_id: Optional[int] = None

    @property
    def summary_image_id(self):
        return self._summary_image_id

    @summary_image_id.setter
    def summary_image_id(self, value):
        if self._summary_image_id is not None:
            raise RuntimeError(f"Summary image id already set to {self._summary_image_id}!")
        if value is not None:
            self._summary_image_id = int(value)

    def write(self, *args, **kwargs):
        self._console_handler.stream.write(*args, **kwargs)
        self._file_handler.stream.write(*args, **kwargs)

    def __enter__(self):
        sys.stdout = self
        sys.stderr = self
        return self

    def __exit__(self, *_):
        # Close file handler and reset sys.stdout and sys.stderr
        self._file_handler.close()
        sys.stdout = self._stdout
        sys.stderr = self._stderr

        # Upload log file to summary image
        if (
            self.summary_image_id
            and os.path.isfile(self._log_filename)
            and os.stat(self._log_filename).st_size
        ):
            try:
                for _ in upload_attachment(self._api, self.summary_image_id, self._log_filename):
                    pass
            except Exception:
                pass


def wait_for_thumbs(
    tator_api: TatorApi, project_id: int, wait_list: List[Tuple[datetime, int, str]]
) -> List[Tuple[datetime, int, str]]:
    # Wait for imports to generate thumbnails
    logger.info("Waiting for transcodes to generate thumbnails for all uploads...")
    wait_list_lookup = {item[1]: item for item in wait_list}
    created_ids = list(wait_list_lookup.keys())
    wait_time = 15  # seconds
    no_change_time = 300  # seconds
    successes = []
    change_dt = datetime.now()
    n_waiting_on = len(created_ids)
    while created_ids:
        iter_start_dt = datetime.now()
        curr_len = len(created_ids)
        logger.info("Media gif thumbnail creation not complete for %d media", curr_len)
        completed_transcodes = []
        if n_waiting_on != curr_len:
            change_dt = iter_start_dt
            n_waiting_on = curr_len
        elif (iter_start_dt - change_dt).total_seconds() > no_change_time:
            # Check transcode status
            change_dt = iter_start_dt
            logger.info("Checking transcode status for %d media", n_waiting_on)
            for media_id in created_ids:
                transcode_id = wait_list_lookup[media_id][2]
                if transcode_id:
                    transcode = tator_api.get_transcode(transcode_id)
                    if transcode and hasattr(transcode, "job") and hasattr(transcode, "spec"):
                        status = transcode.job.status.lower()
                        if status in ["succeeded", "failed", "error"]:
                            logger.debug(
                                "Transcode completed for media '%s' before gifs found", media_id
                            )
                            completed_transcodes.append(media_id)
                        else:
                            logger.debug("Transcode not completed for media '%s'", media_id)
                else:
                    # If the media is not currently transcoding, mark it as complete, so it is only
                    # checked one more time
                    completed_transcodes.append(media_id)

        media_list = []
        try:
            media_list = tator_api.get_media_list_by_id(
                project_id, media_id_query={"ids": created_ids}
            )
        except Exception:
            logger.warning("Could not get media list")

        for media in media_list:
            if getattr(media.media_files, "thumbnail_gif", None):
                # Remove the id from the list to check
                logger.debug("Media gif thumbnail creation complete for media %d", media.id)
                created_ids.remove(media.id)
                successes.append(wait_list_lookup[media.id])

        # After a final check for gifs, remove completed_transcodes from the list
        for media_id in completed_transcodes:
            if media_id in created_ids:
                logger.debug("Transcode completed unsuccessfully for media '%s'", media_id)
                created_ids.remove(media_id)

        if created_ids:
            sleep(wait_time)

    return successes


def list_o2_files(directory: str, skip_decrypt: bool) -> List[str]:
    name_pattern = f"*.mp4" if skip_decrypt else f"*.video-[0-9]*"
    return glob(os.path.join(directory, name_pattern))


def list_b3_files(directory: str) -> List[str]:
    return glob(os.path.join(directory, "*.mp4"))
