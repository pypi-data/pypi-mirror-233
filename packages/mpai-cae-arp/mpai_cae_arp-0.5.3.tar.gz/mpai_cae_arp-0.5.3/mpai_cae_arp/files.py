"""Handle files operations."""

import json
from enum import Enum
from io import TextIOWrapper
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel


class FileAction(str, Enum):
    """The action to perform on the file at opening.

    It can be one of the following:

    - ``r``: read
    - ``w``: write
    - ``a``: append

    """

    READ = "r"
    WRITE = "w"
    APPEND = "a"


class FileType(str, Enum):
    """The file type.

    It can be one of the following:

    - ``yaml``
    - ``json``

    """

    YAML = "yaml"
    JSON = "json"


Encoding = Literal["utf-8"]


class File(BaseModel):
    """Class representing a file, with its path, encoding and format."""

    encoding: Encoding = "utf-8"
    format: FileType  # noqa: A003
    path: str

    def open(self, action: FileAction) -> TextIOWrapper:  # noqa: A003
        """Open the file with the given action.

        Parameters
        ----------
        action : FileAction
            the action to perform on the file at opening

        Returns
        -------
        TextIOWrapper
            the file descriptor

        """
        return Path(self.path).open(  # noqa: SIM115
            mode=action.value,
            encoding=self.encoding,
        )

    def get_content(self) -> dict:
        """Return the file content.

        Raises
        ------
        ValueError
            if the format is not supported

        Returns
        -------
        dict
            the parsed content of the file

        """
        with self.open(FileAction.READ) as filep:
            if self.format == FileType.YAML:
                content = yaml.safe_load(filep)
                return content
            if self.format == FileType.JSON:
                content = json.load(filep)
            else:
                msg = "Format not supported"
                raise ValueError(msg)

        return content

    def write_content(self, content: dict | str) -> None:
        """Write the given content in the file.

        Parameters
        ----------
        content : dict | str
            the content to write in the file
            if content is a string, it will be parsed as a JSON string

        """
        if isinstance(content, str):
            try:
                content = json.loads(json.loads(content))
            except json.decoder.JSONDecodeError as exc:
                msg = "Content str is not a valid JSON string"
                raise ValueError(msg) from exc

        with self.open(FileAction.WRITE) as filep:
            if self.format == FileType.YAML:
                yaml.safe_dump(content, filep)
            elif self.format == FileType.JSON:
                json.dump(content, filep, indent=4)
            else:
                msg = "Format not supported"
                raise ValueError(msg)
