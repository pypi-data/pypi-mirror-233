from datetime import datetime
from typing import Union


def current_timestamp_utc(timespec: str = "seconds") -> Union[float, int]:
    current_timestamp = datetime.now().timestamp()

    return int(current_timestamp) if timespec == "seconds" else current_timestamp


def timestamp_utc_before_n_seconds(n: int, timespec: str = "seconds") -> Union[float, int]:
    return current_timestamp_utc(timespec) - n
