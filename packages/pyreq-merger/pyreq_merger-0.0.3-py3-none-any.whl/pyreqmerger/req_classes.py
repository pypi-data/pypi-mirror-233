import re

from pyreqmerger.file_handler import FileHandler


class ReqContent:
    raw: str = ""
    data: dict = {}

    def __init__(self, content: str) -> None:
        self.raw = content
        self._parse_content()

    def _parse_content(self) -> None:
        self.data = {}

        for match in re.findall(r".*==\d+\.\d+\.\d+", self.raw):
            version = re.search(r"\d+\.\d+\.\d+", match)
            package = re.search(r"(.*)(==)", match)

            if not package or not version:
                return

            self.data[package.group(1)] = version.group(0)


class ReqFileHandler(FileHandler):
    req_content: ReqContent

    def __init__(self, path: str) -> None:
        super().__init__(path)

        if self.valid:
            self.req_content = ReqContent(self.content)
