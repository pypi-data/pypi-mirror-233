from typing import Optional

from connectify.datetime_services import current_timestamp_utc


class NotAFutureDateException(Exception):
    def __init__(self, message: str = None, timestamp: Optional[int] = None):
        self.message = message
        if not self.message:
            self.message = f"Timestamp should be greater then {current_timestamp_utc()}"
        if timestamp and message:
            self.message = f"{message}: Given {timestamp}, should be greater then {current_timestamp_utc()}"

    def __str__(self):
        return self.message
