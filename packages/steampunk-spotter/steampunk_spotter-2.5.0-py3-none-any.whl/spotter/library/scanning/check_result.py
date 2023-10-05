"""Provide check result model."""

import re
from typing import Dict, Any, Optional

import pydantic.dataclasses
from colorama import Fore, Style

from spotter.library.rewriting.models import RewriteSuggestion, CheckType
from spotter.library.scanning.check_catalog_info import CheckCatalogInfo
from spotter.library.scanning.display_level import DisplayLevel
from spotter.library.scanning.item_metadata import ItemMetadata


@pydantic.dataclasses.dataclass
class CheckResult:
    """A container for parsed check results originating from the backend."""

    correlation_id: str
    original_item: Dict[str, Any]
    metadata: Optional[ItemMetadata]
    catalog_info: CheckCatalogInfo
    level: DisplayLevel
    message: str
    suggestion: Optional[RewriteSuggestion]
    doc_url: Optional[str]
    check_type: CheckType

    def construct_output(
        self, disable_colors: bool = False, disable_docs_url: bool = False, disable_rewritable: bool = False
    ) -> str:
        """
        Construct CheckResult output using its properties.

        :param disable_colors: Disable output colors and styling
        :param disable_docs_url: Disable outputting URL to documentation
        :param disable_rewritable: Disable showing check result as rewritable even if it can be rewritten
        :return: Formatted output for check result
        """
        # or: we can have results that relate to Environment - no file and position
        metadata = self.metadata or ItemMetadata(file_name="", line=0, column=0)
        result_level = self.level.name.strip().upper()
        file_location = f"{metadata.file_name}:{metadata.line}:{metadata.column}"

        if self.catalog_info.event_subcode:
            out_prefix = (
                f"{file_location}: {result_level}: "
                f"[{self.catalog_info.event_code}::{self.catalog_info.event_subcode}]"
            )
        else:
            out_prefix = f"{file_location}: {result_level}: [{self.catalog_info.event_code}]"

        out_message = self.message.strip()
        if not disable_colors:
            if result_level == DisplayLevel.ERROR.name:
                out_prefix = Fore.RED + out_prefix + Fore.RESET
                out_message = re.sub(
                    r"'([^']*)'", Style.BRIGHT + Fore.RED + r"\1" + Fore.RESET + Style.NORMAL, out_message
                )
            elif result_level == DisplayLevel.WARNING.name:
                out_prefix = Fore.YELLOW + out_prefix + Fore.RESET
                out_message = re.sub(
                    r"'([^']*)'", Style.BRIGHT + Fore.YELLOW + r"\1" + Fore.RESET + Style.NORMAL, out_message
                )
            else:
                out_message = re.sub(r"'([^']*)'", Style.BRIGHT + r"\1" + Style.NORMAL, out_message)

        if self.suggestion and not disable_rewritable:
            out_rewritable = "(rewritable)"
            if not disable_colors:
                out_rewritable = f"({Fore.MAGENTA}rewritable{Fore.RESET})"
            out_prefix = f"{out_prefix} {out_rewritable}"

        output = f"{out_prefix} {out_message}".strip()
        if not output.endswith("."):
            output += "."
        if not disable_docs_url and self.doc_url:
            out_docs = f"View docs at {self.doc_url}."
            if not disable_colors:
                out_docs = f"View docs at {Fore.CYAN}{self.doc_url}{Fore.RESET}."
            output = f"{output} {out_docs}"

        return output
