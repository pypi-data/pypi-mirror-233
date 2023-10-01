from typing import Union
from pathlib import Path

from dotenv import load_dotenv


def load_env_variables_from_file(file_path: Union[str, Path]) -> None:
    load_dotenv(str(file_path))
