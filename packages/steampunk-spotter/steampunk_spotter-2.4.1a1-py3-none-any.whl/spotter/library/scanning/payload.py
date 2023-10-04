"""Provide scan payload model."""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

import pydantic.dataclasses

from spotter.library.compat.pydantic import compat_to_jsonable_python
from spotter.library.environment import Environment
from spotter.library.parsing.parsing import ParsingResult


@pydantic.dataclasses.dataclass
class Payload:
    """A container for information about the scan payload/input."""

    environment: Environment
    tasks: List[Dict[str, Any]]
    playbooks: List[Dict[str, Any]]

    @classmethod
    def from_json_file(cls, import_path: Path) -> "Payload":
        """
        Load ScanPayload object from JSON file.

        :param import_path: File path with JSON to import from
        :return: ScanPayload object holding input tuple (environment, tasks, playbooks)
        """
        try:
            if not import_path.exists():
                print(f"Error: import file at {import_path} does not exist.", file=sys.stderr)
                sys.exit(2)

            with import_path.open("r", encoding="utf-8") as import_file:
                scan_payload = json.load(import_file)
                environment_dict = scan_payload.get("environment", None)
                if environment_dict is not None:
                    environment = Environment(**environment_dict)
                else:
                    environment = Environment()

                return cls(
                    environment=environment,
                    tasks=scan_payload.get("tasks", []),
                    playbooks=scan_payload.get("playbooks", []),
                )
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(2)

    @classmethod
    def from_args(
        cls,
        parsing_result: ParsingResult,
        environment: Environment,
        include_metadata: bool,
        import_payload: Optional[Path],
    ) -> "Payload":
        """
        Convert CLI arguments to ScanPayload object.

        :param parsing_result: ParsingResult object
        :param environment: Environment object
        :param include_metadata: Upload metadata (i.e., file names, line and column numbers)
        :param import_payload: Path to file where ScanPayload can be imported from
        :return: ScanPayload object
        """
        if import_payload:
            return cls.from_json_file(import_payload)

        return cls(
            environment=environment,
            tasks=parsing_result.tasks if include_metadata else parsing_result.tasks_without_metadata(),
            playbooks=parsing_result.playbooks if include_metadata else parsing_result.playbooks_without_metadata(),
        )

    def to_json_file(self, export_path: Path) -> None:
        """
        Export scan payload to JSON file.

        :param export_path: File path to export to (will be overwritten if exists)
        """
        try:
            with export_path.open("w", encoding="utf-8") as export_file:
                json.dump(compat_to_jsonable_python(self), export_file, indent=2)
        except TypeError as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(2)
