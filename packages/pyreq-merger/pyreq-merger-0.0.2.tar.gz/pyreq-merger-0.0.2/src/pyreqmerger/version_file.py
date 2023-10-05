import re

from pyreqmerger.enums import Errors
from pyreqmerger.file_handler import FileHandler


class VersionFile(FileHandler):
    _version: str = ""

    @property
    def version(self) -> str | Errors:
        if self._version != "":
            return self._version

        if self.content == "":
            return Errors.EMPTY_FILE

        first_line = self.content.split("\n")[0]

        if not re.search(r"\d+\.\d+\.\d+", first_line):
            return Errors.NOT_A_VERSION

        return first_line
