import os
import tempfile
from pathlib import Path
from typing import Optional


class TempFileWithContent:
    def __init__(self, content: str, file_name: Optional[str]):
        self.__file = tempfile.NamedTemporaryFile(mode="w", suffix=file_name, delete=False)
        self.content = content
        self.file_name = file_name
        self.path: Path = Path(self.__file.name)

        with self.__file as output_stream:
            output_stream.write(content)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        os.unlink(self.__file.name)
