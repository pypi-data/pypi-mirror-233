import os


class FileHandler:
    path: str = ""
    _content: str = ""
    _valid: bool = False

    def __init__(self, path: str) -> None:
        self.path = path

    def __str__(self) -> str:
        return os.path.basename(self.path)

    @property
    def valid(self) -> bool:
        if not self._valid:
            self._valid = os.path.isfile(self.path)

            if self._valid:
                self.path = os.path.abspath(self.path)

        return self._valid

    @property
    def content(self) -> str:
        if self._content == "":
            with open(self.path, "r", encoding="utf-8") as file:
                self._content = file.read()

        return self._content

    def write(self, content: str) -> None:
        with open(self.path, "w", encoding="utf-8") as file:
            file.write(content)

    @property
    def self_delete(self) -> None:
        os.remove(self.path)
