import json
import os
from typing import Any, Union

import yaml
from logs.logger import get_logger

logger = get_logger(__name__)


def read_file(
    path: str, is_json: bool = False, is_yaml: bool = False, encoding: str = "utf-8"
) -> Union[dict[str, Any], str]:
    """
    Read file data.

    Params
    ------
    path: File path
    is_json: File is JSON like
    is_yaml: File is YAML like
    encoding: Encoding type
    """
    with open(path, encoding=encoding) as file:
        if is_json:
            return json.load(file)
        elif is_yaml:
            return yaml.safe_load(file)

        return file.read()


def delete_file(path: str) -> None:
    """
    Delete file.

    Params
    ------
    path: File path
    """
    if not os.path.exists(path):
        logger.warning(f"Path does not exist: {path}")
        return

    os.remove(path)
    logger.info(f"File has been deleted: {path}")


def delete_files(path: str, exclude: list[str] = None) -> None:
    """
    Delete all files from the specified folder.

    Params
    ------
    path: path to the folder
    exclude: list of files to exclude
    """
    if not os.path.exists(path):
        logger.warning(f"Path does not exist: {path}")
        return

    files = os.listdir(path)
    for file in files:
        if exclude and file in exclude:
            continue

        os.remove(f"{path}/{file}")

    logger.info(f"Files have been deleted from the {path}")
