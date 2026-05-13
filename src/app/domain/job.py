from enum import StrEnum
from typing import NewType
from uuid import UUID


JobId = NewType("JobId", UUID)


class JobStatus(StrEnum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
