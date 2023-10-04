"""Provide item metadata model."""

from pathlib import Path
from typing import Dict, Any

import pydantic.dataclasses


@pydantic.dataclasses.dataclass
class ItemMetadata:
    """A container for item metadata originating from the original task or play."""

    file_name: str
    line: int
    column: int

    @classmethod
    def from_item_meta(cls, item_meta: Dict[str, Any]) -> "ItemMetadata":
        """
        Convert task metadata to ItemMetadata object for storing metadata for Ansible task or play.

        :param item_meta: Ansible task spotter_metadata content.
        :return: TaskMetadata object
        """
        file_name = item_meta.get("file", "")
        line = item_meta.get("line", "")
        column = item_meta.get("column", "")

        try:
            # trim the part of the directory that is shared with CWD if this is possible
            file_name = str(Path(file_name).relative_to(Path.cwd()))
        except ValueError:
            pass

        return cls(file_name=file_name, line=line, column=column)
