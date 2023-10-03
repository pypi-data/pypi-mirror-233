import tator

from hms_import.b3.upload import run_b3_upload
from hms_import.util import HmsLogHandler


def main(*, host: str, token: str, console_log_level: int, **kwargs):
    tator_api = tator.get_api(host=host, token=token)
    with HmsLogHandler(tator_api=tator_api, console_log_level=console_log_level) as log_handler:
        log_handler.summary_image_id = run_b3_upload(tator_api=tator_api, **kwargs)
