"""Provide scan result model."""

import json
import sys
import xml
from io import StringIO
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, cast

import pydantic.dataclasses
import ruamel.yaml as yaml
from colorama import Fore, Style

from spotter.library.reporting.report import JUnitXml
from spotter.library.rewriting.models import RewriteSuggestion, CheckType
from spotter.library.rewriting.processor import update_files
from spotter.library.scanning.check_catalog_info import CheckCatalogInfo
from spotter.library.scanning.check_result import CheckResult
from spotter.library.scanning.display_level import DisplayLevel
from spotter.library.scanning.item_metadata import ItemMetadata
from spotter.library.scanning.output_format import OutputFormat
from spotter.library.scanning.progress import Progress
from spotter.library.scanning.summary import Summary


@pydantic.dataclasses.dataclass
class Result:
    """A container for scan result originating from the backend."""

    # TODO: Add more fields from scan response if we need them
    # pylint: disable=too-many-instance-attributes
    uuid: Optional[str]
    user: Optional[str]
    user_info: Optional[Dict[str, Any]]
    project: Optional[str]
    environment: Optional[Dict[str, Any]]
    scan_date: Optional[str]
    subscription: Optional[str]
    is_paid: Optional[bool]
    summary: Summary
    scan_progress: Progress
    check_results: List[CheckResult]
    fixed_check_results: List[CheckResult]

    @classmethod
    def from_api_response(
        cls,
        response_json: Dict[str, Any],
        input_tasks: List[Dict[str, Any]],
        input_playbooks: List[Dict[str, Any]],
        scan_time: float,
    ) -> "Result":
        """
        Convert scan API response to Result object.

        :param response_json: The backend API response in JSON format
        :param input_tasks: The scanned tasks with no information removed
        :param input_playbooks: The scanned playbooks with plays that have no information removed
        :param scan_time: Time taken to do a scan
        :return: Result object
        """
        scan_result = cls(
            uuid=response_json.get("id", ""),
            user=response_json.get("user", ""),
            user_info=response_json.get("user_info", {}),
            project=response_json.get("project", ""),
            environment=response_json.get("environment", {}),
            scan_date=response_json.get("scan_date", ""),
            subscription=response_json.get("subscription", ""),
            is_paid=response_json.get("is_paid", False),
            summary=Summary(
                scan_time=scan_time, num_errors=0, num_warnings=0, num_hints=0, status=response_json.get("status", "")
            ),
            scan_progress=Progress.from_api_response_element(response_json.get("scan_progress", {})),
            check_results=[],
            fixed_check_results=[],
        )
        scan_result.parse_check_results(response_json, input_tasks, input_playbooks)
        return scan_result

    @staticmethod
    def _parse_known_check_result(
        element: Dict[str, Any], input_items: Dict[str, Dict[str, Any]]
    ) -> Optional[CheckResult]:
        check_type: CheckType = CheckType.from_string(element.get("check_type", ""))
        if check_type not in [CheckType.TASK, CheckType.PLAY]:
            print(
                f"Error: incorrect check type '{check_type}'. Should be one of [{CheckType.TASK},{CheckType.PLAY}]",
                file=sys.stderr,
            )
            sys.exit(2)

        correlation_id = element.get("correlation_id")
        if not correlation_id:
            print(
                "Error: correlation id for result was not set. This should not happen for a task or play.",
                file=sys.stderr,
            )
            sys.exit(2)

        # guard against incomplete results where we don't match a task or play
        original_item = input_items.get(correlation_id)
        if not original_item:
            print("Could not map task ID to its original task.")
            return None

        # guard against missing task or play args and metadata
        item_meta = original_item.get("spotter_metadata", None)
        if not item_meta:
            print("Meta data is missing.")
            return None

        suggestion = element.get("suggestion", "")
        item_metadata_object = ItemMetadata.from_item_meta(item_meta)
        display_level = DisplayLevel.from_string(element.get("level", ""))

        suggestion_object: Optional[RewriteSuggestion] = RewriteSuggestion.from_item(
            check_type, original_item, suggestion, display_level
        )

        result = CheckResult(
            correlation_id=correlation_id,
            original_item=original_item,
            metadata=item_metadata_object,
            catalog_info=CheckCatalogInfo.from_api_response_element(element),
            level=display_level,
            message=element.get("message", ""),
            suggestion=suggestion_object,
            doc_url=element.get("doc_url", ""),
            check_type=check_type,
        )
        return result

    @staticmethod
    def _parse_unknown_check_result(element: Dict[str, Any]) -> CheckResult:
        check_type = CheckType.from_string(element.get("check_type", ""))
        display_level = DisplayLevel.from_string(element.get("level", ""))
        check_catalog_info = CheckCatalogInfo.from_api_response_element(element)

        result = CheckResult(
            correlation_id="",
            original_item={},
            metadata=None,
            catalog_info=check_catalog_info,
            level=display_level,
            message=element.get("message", ""),
            suggestion=None,
            doc_url=element.get("doc_url", ""),
            check_type=check_type,
        )
        return result

    def parse_check_results(
        self, response_json: Dict[str, Any], input_tasks: List[Dict[str, Any]], input_playbooks: List[Dict[str, Any]]
    ) -> None:
        """
        Parse result objects and map tasks with complete information.

        :param response_json: The backend API response in JSON format
        :param input_tasks: The scanned tasks with no information removed
        :param input_playbooks: The scanned playbooks with plays that have no information removed
        """
        tasks_as_dict = {x["task_id"]: x for x in input_tasks if "task_id" in x}
        plays_as_dict = {}
        for playbook in input_playbooks:
            plays_as_dict.update({x["play_id"]: x for x in playbook["plays"] if "play_id" in x})

        result: List[CheckResult] = []
        for element in response_json.get("elements", []):
            check_type = CheckType.from_string(element.get("check_type", ""))
            item: Optional[CheckResult] = None

            if check_type == CheckType.TASK:
                item = self._parse_known_check_result(element, tasks_as_dict)
            elif check_type == CheckType.PLAY:
                item = self._parse_known_check_result(element, plays_as_dict)
            else:
                item = self._parse_unknown_check_result(element)

            if item:
                self.summary.update(item)
                result.append(item)
        self.check_results = result

    def filter_check_results(self, threshold: DisplayLevel) -> None:
        """
        Filter a list of check results by only keeping tasks over a specified severity level.

        :param threshold: The DisplayLevel object as threshold (inclusive) of what level messages (and above) to keep
        """
        self.check_results = [cr for cr in self.check_results if cr.level.value >= threshold.value]

    @staticmethod
    def _get_sort_key(check_result: CheckResult) -> Tuple[str, int, int, int]:
        """
        Extract a tuple of file name, line number, column number and negative display level from check result.

        This is a key function for sorting check results.

        :param check_result: CheckResult object
        :return: A tuple of file name, line number, column number, and negative display level
        """
        if not check_result.metadata:
            return "", 0, 0, 0
        return (
            check_result.metadata.file_name,
            int(check_result.metadata.line),
            int(check_result.metadata.column),
            -check_result.level.value,
        )

    def sort_check_results(self) -> None:
        """Sort a list of check results by file names (alphabetically) and also YAML line and column numbers."""
        self.check_results.sort(key=self._get_sort_key)

    # TODO: Refactor this function to multiple smaller functions
    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements
    def _format_text(self, disable_colors: bool = False, disable_docs_url: bool = False, rewrite: bool = False) -> str:
        """
        Format scan result as text.

        :param disable_colors: Disable output colors and styling
        :param disable_docs_url: Disable outputting URL to documentation
        :param rewrite: Rewrite files with fixes
        :return: A formatted string
        """
        output = ""

        fixed_check_results_label = ""
        fixed_check_results = ""
        if self.fixed_check_results:
            fixed_check_results_label = "Rewritten check results"
            for result_fixed in self.fixed_check_results:
                fixed_check_results += result_fixed.construct_output(disable_colors, disable_docs_url, True) + "\n"

        check_results_label = ""
        check_results = ""
        if self.check_results:
            if self.fixed_check_results:
                check_results_label = "Remaining check results"
            else:
                check_results_label = "Check results"
        for result in self.check_results:
            check_results += result.construct_output(disable_colors, disable_docs_url) + "\n"

        def level_sort_key(level: DisplayLevel) -> int:
            return cast(int, level.value)

        worst_level = DisplayLevel.SUCCESS
        scan_summary_label = "Scan summary"
        if len(self.check_results) > 0:
            worst_level = max((cr.level for cr in self.check_results), key=level_sort_key)

        if rewrite:
            suggestion_level_file_tuples = [
                (cr.suggestion, cr.metadata.file_name)
                for cr in self.fixed_check_results
                if cr.suggestion is not None and cr.metadata is not None
            ]
        else:
            suggestion_level_file_tuples = [
                (cr.suggestion, cr.metadata.file_name)
                for cr in self.check_results
                if cr.suggestion is not None and cr.metadata is not None
            ]
        rewrite_files_len = len(set(t[1] for t in suggestion_level_file_tuples))
        rewrite_message = (
            f"{'Did' if rewrite else 'Can'} rewrite {rewrite_files_len} file(s) with "
            f"{len(suggestion_level_file_tuples)} change(s)."
        )
        time_message = f"Spotter took {self.summary.scan_time:.3f} s to scan your input."
        stats_message = (
            f"It resulted in {self.summary.num_errors} error(s), {self.summary.num_warnings} "
            f"warning(s) and {self.summary.num_hints} hint(s)."
        )
        overall_status_message = f"Overall status: {worst_level.name.upper()}"

        if not disable_colors:
            if fixed_check_results_label:
                fixed_check_results_label = f"{Style.BRIGHT}{fixed_check_results_label}{Style.NORMAL}"
            if check_results_label:
                check_results_label = f"{Style.BRIGHT}{check_results_label}{Style.NORMAL}"
            if scan_summary_label:
                scan_summary_label = f"{Style.BRIGHT}{scan_summary_label}{Style.NORMAL}"
            time_message = (
                f"Spotter took {Style.BRIGHT}{self.summary.scan_time:.3f} s{Style.NORMAL} to scan " f"your input."
            )
            stats_message = (
                f"It resulted in {Style.BRIGHT + Fore.RED}{self.summary.num_errors} error(s)"
                f"{Fore.RESET + Style.NORMAL}, {Style.BRIGHT + Fore.YELLOW}{self.summary.num_warnings} "
                f"warning(s){Fore.RESET + Style.NORMAL} and {Style.BRIGHT}{self.summary.num_hints} "
                f"hint(s){Style.NORMAL}."
            )
            rewrite_message = (
                f"{'Did' if rewrite else 'Can'} {Style.BRIGHT + Fore.MAGENTA}rewrite{Fore.RESET + Style.NORMAL} "
                f"{Style.BRIGHT}{rewrite_files_len} file(s){Style.NORMAL} with "
                f"{Style.BRIGHT}{len(suggestion_level_file_tuples)} change(s){Style.NORMAL}."
            )

            if worst_level == DisplayLevel.ERROR:
                overall_status_message = (
                    f"Overall status: {Style.BRIGHT + Fore.RED}{worst_level.name.upper()}{Fore.RESET + Style.NORMAL}"
                )
            elif worst_level == DisplayLevel.WARNING:
                overall_status_message = (
                    f"Overall status: {Style.BRIGHT + Fore.YELLOW}{worst_level.name.upper()}{Fore.RESET + Style.NORMAL}"
                )
            elif worst_level == DisplayLevel.HINT:
                overall_status_message = f"Overall status: {Style.BRIGHT}{worst_level.name.upper()}{Style.NORMAL}"
            else:
                overall_status_message = (
                    f"Overall status: {Style.BRIGHT + Fore.GREEN}{worst_level.name.upper()}{Fore.RESET + Style.NORMAL}"
                )

        if self.fixed_check_results and self.check_results:
            output += (
                f"{fixed_check_results_label}:\n{fixed_check_results}\n{check_results_label}:\n"
                f"{check_results}\n{scan_summary_label}:\n{time_message}\n{stats_message}\n"
                f"{rewrite_message}\n{overall_status_message}"
            )
        elif self.fixed_check_results:
            output += (
                f"{fixed_check_results_label}:\n{fixed_check_results}\n{scan_summary_label}:\n{time_message}"
                f"\n{stats_message}\n{rewrite_message}\n{overall_status_message}"
            )
        elif self.check_results:
            output += (
                f"{check_results_label}:\n{check_results}\n{scan_summary_label}:\n{time_message}\n"
                f"{stats_message}\n{rewrite_message}\n{overall_status_message}"
            )
        else:
            output += (
                f"{scan_summary_label}:\n{time_message}\n{stats_message}\n{rewrite_message}\n{overall_status_message}"
            )

        return output

    def _format_dict(self, disable_docs_url: bool = False) -> Dict[str, Any]:
        """
        Format scan result as Python dict.

        :param disable_docs_url: Disable outputting URL to documentation
        :return: A formatted string
        """
        check_result_outputs = []
        for result in self.check_results:
            metadata = result.metadata or ItemMetadata(file_name="", line=0, column=0)
            catalog_info = result.catalog_info
            suggestion_dict = {}
            if result.suggestion:
                suggestion_dict = {
                    "start_mark": result.suggestion.start_mark,
                    "end_mark": result.suggestion.end_mark,
                    "suggestion": result.suggestion.suggestion_spec,
                }

            check_result_outputs.append(
                {
                    "task_id": result.correlation_id,  # It is here because we want to be back compatible
                    "file": metadata.file_name,
                    "line": metadata.line,
                    "column": metadata.column,
                    "check_class": catalog_info.check_class,
                    "event_code": catalog_info.event_code,
                    "event_value": catalog_info.event_value,
                    "event_message": catalog_info.event_message,
                    "event_subcode": catalog_info.event_subcode,
                    "event_submessage": catalog_info.event_submessage,
                    "level": result.level.name.strip(),
                    "message": result.message.strip(),
                    "suggestion": suggestion_dict,
                    "doc_url": None if disable_docs_url else result.doc_url,
                    "correlation_id": result.correlation_id,
                    "check_type": result.check_type.name.strip(),
                }
            )

        return {
            "uuid": self.uuid,
            "user": self.user,
            "user_info": self.user_info,
            "project": self.project,
            "environment": self.environment,
            "scan_date": self.scan_date,
            "subscription": self.subscription,
            "is_paid": self.is_paid,
            "summary": {
                "scan_time": self.summary.scan_time,
                "num_errors": self.summary.num_errors,
                "num_warnings": self.summary.num_warnings,
                "num_hints": self.summary.num_hints,
                "status": self.summary.status,
            },
            "scan_progress": {
                "progress_status": str(self.scan_progress.progress_status),
                "current": self.scan_progress.current,
                "total": self.scan_progress.total,
            },
            "check_results": check_result_outputs,
        }

    def _format_json(self, disable_docs_url: bool = False) -> str:
        """
        Format scan result as JSON.

        :param disable_docs_url: Disable outputting URL to documentation
        :return: A formatted string
        """
        return json.dumps(self._format_dict(disable_docs_url), indent=2)

    def _format_yaml(self, disable_docs_url: bool = False) -> str:
        """
        Format scan result as YAML.

        :param disable_docs_url: Disable outputting URL to documentation
        :return: A formatted string
        """
        stream = StringIO()
        yaml.round_trip_dump(self._format_dict(disable_docs_url), stream=stream, indent=2, default_flow_style=False)
        return stream.getvalue()

    def format_junit_xml(self, disable_docs_url: bool = False) -> str:
        """
        Format scan result as JUnitXML.

        :param disable_docs_url: Disable outputting URL to documentation
        :return: A formatted string
        """
        try:
            junit_renderer = JUnitXml()
            return junit_renderer.render(self.check_results, disable_docs_url)
        except xml.parsers.expat.ExpatError as e:
            print(f"Error: exporting JUnit XML failed: {e}.", file=sys.stderr)
            sys.exit(2)

    def format_output(
        self,
        output_format: OutputFormat,
        disable_colors: bool = False,
        disable_docs_url: bool = False,
        rewrite: bool = False,
    ) -> str:
        """
        Format scan result.

        :param output_format: Target output format
        :param disable_colors: Disable output colors and styling
        :param disable_docs_url: Disable outputting URL to documentation
        :param rewrite: Rewrite files with fixes
        :return: A formatted string
        """
        if output_format == OutputFormat.TEXT:
            return self._format_text(disable_colors, disable_docs_url, rewrite)
        if output_format == OutputFormat.JSON:
            return self._format_json(disable_docs_url)
        if output_format == OutputFormat.YAML:
            return self._format_yaml(disable_docs_url)

        print(
            f"Error: unknown output format: {output_format}, "
            f"valid values are: {list(str(e) for e in OutputFormat)}.",
            file=sys.stderr,
        )
        sys.exit(2)

    def apply_check_result_suggestions(self, scan_paths: List[Path], display_level: DisplayLevel) -> None:
        """
        Automatically apply suggestions.

        :param scan_paths: A list of original paths to Ansible artifacts provided for scanning
        :param display_level: DisplayLevel object
        """
        all_suggestions = [cr.suggestion for cr in self.check_results if cr.suggestion is not None]

        # TODO: Remove when we find a solution for accessing original paths to Ansible artifacts provided for scanning
        for suggestion in all_suggestions:
            suggestion.file_parent = suggestion.file.parent
            for scan_path in scan_paths:
                if scan_path in (scan_path / suggestion.file).parents:
                    suggestion.file_parent = scan_path
                    break

        applied_suggestions = update_files(all_suggestions, display_level)
        self.fixed_check_results = [
            cr for cr in self.check_results if cr.suggestion is not None and cr.suggestion in applied_suggestions
        ]
        self.check_results = [cr for cr in self.check_results if cr not in self.fixed_check_results]
