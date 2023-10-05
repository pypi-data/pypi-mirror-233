from __future__ import annotations

from enum import Enum


class MergeMethod(Enum):
    UPGRADE = "upgrade"
    DOWNGRADE = "downgrade"

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def from_str(method: str) -> MergeMethod:
        match method.lower():
            case "upgrade":
                return MergeMethod.UPGRADE

            case "downgrade":
                return MergeMethod.DOWNGRADE

            case _:
                return MergeMethod.UPGRADE


class Errors(Enum):
    OK = "OK"
    EMPTY_FILE = "File contents are empty"
    NOT_A_VERSION = "Content found is not a valid version"
    INVALID_FILE_PATH = "File path does not exist"

    def __str__(self) -> str:
        return self.value
