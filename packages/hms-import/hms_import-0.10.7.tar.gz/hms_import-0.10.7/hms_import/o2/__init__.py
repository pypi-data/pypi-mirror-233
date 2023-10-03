from configparser import ConfigParser

import tator

from hms_import.o2.upload import run_o2_upload
from hms_import.util import HmsLogHandler


def main(console_log_level: int, config_file: str):
    config = ConfigParser()
    config.read(config_file)
    host = config["Tator"]["Host"]
    token = config["Tator"]["Token"]
    tator_api = tator.get_api(host=host, token=token)
    with HmsLogHandler(tator_api=tator_api, console_log_level=console_log_level) as log_handler:
        log_handler.summary_image_id = run_o2_upload(tator_api=tator_api, config=config)
