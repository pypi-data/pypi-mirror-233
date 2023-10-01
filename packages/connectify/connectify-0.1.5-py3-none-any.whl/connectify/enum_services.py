import enum


class APIResponseEnum(str, enum.Enum):
    SUCCESS = 'success'
    ERROR = "error"
    FAILURE = "failure"
