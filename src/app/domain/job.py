from enum import StrEnum
from typing import NewType


JobId = NewType("JobId", str)


class JobStatus(StrEnum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
