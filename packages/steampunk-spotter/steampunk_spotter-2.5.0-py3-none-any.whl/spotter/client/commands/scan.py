"""Provide scan CLI command."""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.style import Style
from rich.theme import Theme

from spotter.library.api import ApiClient
from spotter.library.compat.pydantic import compat_to_jsonable_python
from spotter.library.environment import Environment
from spotter.library.parsing.noqa_comments import SpotterNoqa
from spotter.library.parsing.parsing import parse_ansible_artifacts, ParsingResult
from spotter.library.scanning.display_level import DisplayLevel
from spotter.library.scanning.output_format import OutputFormat
from spotter.library.scanning.payload import Payload
from spotter.library.scanning.profile import Profile
from spotter.library.scanning.progress import Progress as ScanProgress
from spotter.library.scanning.progress_status import ProgressStatus as ScanProgressStatus
from spotter.library.scanning.result import Result
from spotter.library.scanning.start_async import StartAsync
from spotter.library.storage import Storage


def add_parser(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    """
    Add a new scan command parser to subparsers.

    :param subparsers: Subparsers action
    """
    parser = subparsers.add_parser("scan", help="Initiate Ansible scan", description="Initiate Ansible scan")
    parser.add_argument(
        "--project-id",
        "-p",
        type=str,
        help="UUID of an existing project (default project from " "default organization will be used if not specified)",
    )
    parser.add_argument("--config", "-c", type=lambda p: Path(p).absolute(), help="Configuration file (as JSON/YAML)")
    parser.add_argument(
        "--option", "-o", type=lambda s: s.strip().split("="), action="append", default=[], help=argparse.SUPPRESS
    )
    parser.add_argument(
        "--ansible-version",
        type=str,
        choices=[
            "2.0",
            "2.1",
            "2.2",
            "2.3",
            "2.4",
            "2.5",
            "2.6",
            "2.7",
            "2.8",
            "2.9",
            "2.10",
            "2.11",
            "2.12",
            "2.13",
            "2.14",
            "2.15",
        ],
        metavar="[2.0, 2.15]",
        help="Target Ansible version to scan against (e.g., 2.14). If not specified, Spotter will try to discover the "
        "Ansible version installed on your system. If not found, all Ansible versions are considered for scanning.",
    )
    parser.add_argument(
        "--exclude-values", action="store_true", help="Omit parsing and uploading values from Ansible playbooks"
    )
    parser.add_argument("--include-values", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--upload-values", dest="include_values", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument(
        "--exclude-metadata",
        action="store_true",
        help="Omit collecting and uploading metadata (i.e., file names, line and column numbers)",
    )
    parser.add_argument("--include-metadata", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--upload-metadata", dest="include_metadata", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--rewrite", "-r", action="store_true", help="Rewrite files with fixes")
    parser.add_argument(
        "--display-level",
        "-l",
        type=DisplayLevel.from_string,
        choices=[DisplayLevel.HINT, DisplayLevel.WARNING, DisplayLevel.ERROR],
        default=DisplayLevel.HINT,
        help="Display only check results with specified level or greater "
        "(e.g., -l warning will show all warnings and errors, but suppress hints)",
    )
    parser.add_argument(
        "--profile",
        type=Profile.from_string,
        choices=list(Profile),
        default=Profile.DEFAULT,
        help="Set profile with selected set of checks to be used for scanning",
    )
    parser.add_argument(
        "--skip-checks",
        nargs="?",
        action="append",
        default=[],
        help="Skip checks with specified IDs (e.g., --skip-checks E101,H500,W1800)",
    )
    parser.add_argument(
        "--enforce-checks",
        nargs="?",
        action="append",
        default=[],
        help="Enforce checks with specified IDs (e.g., --enforce-checks E001,W400,H904)",
    )
    parser.add_argument("--no-docs-url", action="store_true", help="Disable outputting URLs to documentation")
    parser.add_argument("--no-progress", action="store_true", help="Disable showing scanning progress")
    parser.add_argument(
        "--junit-xml",
        type=lambda p: Path(p).absolute(),
        help="Output file path to export the scan result to a file in JUnit XML format",
    )
    parser.add_argument(
        "--format",
        "-f",
        type=OutputFormat.from_string,
        choices=list(OutputFormat),
        default=OutputFormat.TEXT,
        help="Output format for the scan result",
    )
    parser.add_argument(
        "--output",
        type=lambda p: Path(p).absolute(),
        help="Output file path where the formatted scan result will be exported to",
    )
    import_export_group = parser.add_mutually_exclusive_group()
    import_export_group.add_argument(
        "--import-payload",
        "-i",
        type=lambda p: Path(p).absolute(),
        help="Path to the previously exported file to be sent for scanning",
    )
    import_export_group.add_argument(
        "--export-payload",
        "-e",
        type=lambda p: Path(p).absolute(),
        help="Output file path to export the locally scanned data without sending anything for scanning at the server",
    )
    parser.add_argument(
        "path", type=lambda p: Path(p).absolute(), nargs="*", help="Path to Ansible artifact or directory"
    )
    parser.set_defaults(func=_parser_callback)


def _parser_callback(args: argparse.Namespace) -> None:
    # pylint: disable=too-many-branches,too-many-locals, too-many-statements
    """
    Execute callback for scan command.

    :param args: Argparse arguments
    """
    api_endpoint = args.endpoint or os.environ.get("SPOTTER_ENDPOINT", "")
    storage_path = args.storage_path or Storage.DEFAULT_PATH
    api_token = args.api_token or os.environ.get("SPOTTER_API_TOKEN")
    username = args.username or os.environ.get("SPOTTER_USERNAME")
    password = args.password or os.environ.get("SPOTTER_PASSWORD")
    debug = args.debug
    scan_paths = args.path

    if args.import_payload and scan_paths:
        print("Error: the --import-payload is mutually exclusive with positional arguments.", file=sys.stderr)
        sys.exit(2)

    if (
        args.export_payload
        and not scan_paths
        or (not args.export_payload and not args.import_payload and not scan_paths)
    ):
        print("Error: no paths provided for scanning.", file=sys.stderr)
        sys.exit(2)

    if args.export_payload and args.exclude_metadata:
        print(
            "Warning: exporting without the metadata will not allow you to properly import payload. "
            "Consider omitting the --exclude-metadata optional argument.",
            file=sys.stderr,
        )

    ansible_version = args.ansible_version
    if args.option:
        print("Warning: the --option optional argument is deprecated. Use specific CLI optional arguments instead.")
        for key_value in args.option:
            if len(key_value) != 2:
                print(f"Error: '{'='.join(key_value)}' extra option is not specified as key=value.", file=sys.stderr)
                sys.exit(2)
            else:
                if not ansible_version and key_value[0] == "ansible_version" and isinstance(key_value[1], str):
                    ansible_version = key_value[1]

    # workaround for a deprecated --format junit_xml
    if args.format == OutputFormat.JUNIT_XML:
        print(
            "Warning: the --format junit_xml is deprecated. Use --junit-xml file.xml instead. "
            "Proceeding with text output and JUnitXML report."
        )
        if args.output:
            args.junit_xml = args.output
            args.format = OutputFormat.TEXT
            args.output = None

    # ensure that colors and showing progress are possible only for text output that will be printed to the console
    if args.output or args.format != OutputFormat.TEXT:
        args.no_colors = True
        args.no_progress = True

    if args.include_values:
        print(
            "Warning: the --include-values optional argument is deprecated. Playbook values are now included by "
            "default. You can exclude them with --exclude-values."
        )
    if args.include_metadata:
        print(
            "Warning: the --include-metadata optional argument is deprecated. Metadata (i.e., file names, line and "
            "column numbers) is now included by default. You can exclude it with --exclude-metadata."
        )

    scan(
        api_endpoint,
        storage_path,
        api_token,
        username,
        password,
        args.no_colors,
        args.no_progress,
        args.project_id,
        args.config,
        ansible_version,
        not args.exclude_values,
        not args.exclude_metadata,
        args.rewrite,
        args.display_level,
        args.profile,
        args.skip_checks,
        args.enforce_checks,
        args.no_docs_url,
        args.format,
        args.output,
        args.junit_xml,
        args.import_payload,
        args.export_payload,
        scan_paths,
        debug=debug,
    )


# pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements
def scan(
    api_endpoint: str,
    storage_path: Path,
    api_token: Optional[str],
    username: Optional[str],
    password: Optional[str],
    no_colors: bool,
    no_progress: bool,
    project_id: Optional[str],
    config_path: Optional[Path],
    ansible_version: Optional[str],
    include_values: bool,
    include_metadata: bool,
    rewrite: bool,
    display_level: DisplayLevel,
    profile: Profile,
    skip_checks: List[str],
    enforce_checks: List[str],
    no_docs_url: bool,
    output_format: OutputFormat,
    output_path: Optional[Path],
    junit_xml: Optional[Path],
    import_payload: Optional[Path],
    export_payload: Optional[Path],
    scan_paths: List[Path],
    debug: bool = False,
) -> None:
    """
    Scan Ansible content and return scan result.

    :param api_endpoint: Steampunk Spotter API endpoint
    :param storage_path: Path to storage
    :param api_token: Steampunk Spotter API token
    :param username: Steampunk Spotter username
    :param password: Steampunk Spotter password
    :param no_colors: Disable output colors
    :param no_progress: Disable showing progress
    :param project_id: UUID of an existing Steampunk Spotter project
    :param config_path: Path to configuration file
    :param ansible_version: Target Ansible version to scan against (e.g., 2.14)
    :param include_values: Parse and upload values from Ansible task parameters to the server
    :param include_metadata: Upload metadata (i.e., file names, line and column numbers) to the server
    :param rewrite: Rewrite files with fixes
    :param display_level: Display only check results with specified level or greater
    :param profile: Profile with selected set of checks to be used for scanning
    :param skip_checks: List of check IDs for checks to be skipped
    :param enforce_checks: List of check IDs for checks to be enforced
    :param no_docs_url: Disable outputting URLs to documentation
    :param junit_xml: Path where JUnit XML report will be exported to
    :param output_format: Output format of the scan result
    :param output_path: Output file path where the formatted scan result will be exported to
    :param import_payload: Path to the previously exported file to be sent for scanning
    :param export_payload: Path to export the locally scanned data without sending anything for scanning to the server
    :param scan_paths: Path to Ansible artifact or directory
    :param debug: Enable debug mode
    """
    # create and set environment
    # the order that we read configuration is the following (in each step we overwrite what the previous one has):
    # 1. local discovery (from user's current workspace)
    # 2. project config file (.spotter.json/.spotter.yml/.spotter.yaml file in the current working directory)
    # 3. config file (JSON/YAML file provided after --config flag)
    # 4. optional CLI arguments (e.g., --ansible-version)
    environment = Environment.from_local_discovery(scan_paths)
    environment = environment.combine(Environment.from_project_configuration_file())
    if config_path:
        environment = environment.combine(Environment.from_config_file(config_path))
    if ansible_version and environment.ansible_version:
        environment.ansible_version.ansible_core = ansible_version

    cli_scan_args_skip_checks = []
    cli_scan_args_enforce_checks = []
    if environment.cli_scan_args:
        cli_scan_args_skip_checks = environment.cli_scan_args.get("skip_checks", [])
        cli_scan_args_enforce_checks = environment.cli_scan_args.get("enforce_checks", [])
    if skip_checks:
        cli_scan_args_skip_checks = []
        for skip_check in skip_checks:
            cli_scan_args_skip_checks.extend(SpotterNoqa.parse_noqa_comment(skip_check, use_noqa_regex=False))
    if enforce_checks:
        cli_scan_args_enforce_checks = []
        for enforce_check in enforce_checks:
            cli_scan_args_enforce_checks.extend(SpotterNoqa.parse_noqa_comment(enforce_check, use_noqa_regex=False))

    environment = environment.combine(
        Environment(
            cli_scan_args={
                "parse_values": include_values,
                # FIXME: Remove this deprecated option that is currently mandatory on backend.
                "include_values": include_values,
                "include_metadata": include_metadata,
                "rewrite": rewrite,
                "display_level": str(display_level),
                "profile": str(profile),
                "skip_checks": cli_scan_args_skip_checks,
                "enforce_checks": cli_scan_args_enforce_checks,
            }
        )
    )

    progress_custom_theme = Theme(
        {
            "bar.pulse": Style(color="rgb(103,174,202)"),
            "bar.complete": Style(color="rgb(103,174,202)"),
            "bar.finished": Style(color="rgb(86,194,133)"),
            "progress.percentage": Style(color="rgb(103,174,202)"),
            "progress.elapsed": Style.null(),
            "progress.remaining": Style.null(),
        }
    )
    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=Console(theme=progress_custom_theme, no_color=no_colors),
    )
    if no_progress:
        progress.disable = True

    with progress:
        progress_task = progress.add_task("Parsing...", total=None)
        if import_payload:
            parsing_result = ParsingResult(tasks=[], playbooks=[])
            scan_payload = Payload.from_args(parsing_result, environment, include_metadata, import_payload)
            parsing_result.tasks = scan_payload.tasks
            parsing_result.playbooks = scan_payload.playbooks
        else:
            parsing_result = parse_ansible_artifacts(scan_paths, parse_values=bool(include_values))
            scan_payload = Payload.from_args(parsing_result, environment, include_metadata, import_payload)

        if export_payload:
            scan_payload.to_json_file(export_payload)

            file_name = str(export_payload)
            try:
                # trim the part of the directory that is shared with CWD if this is possible
                file_name = str(Path(file_name).relative_to(Path.cwd()))
            except ValueError:
                pass

            print(
                f"Scan data saved to {file_name}.\nNote: this operation is fully offline. No actual scan was executed."
            )
            sys.exit(0)
        else:
            storage = Storage(storage_path)

            # TODO: extract this to a separate configuration component along with other configuration file options
            if not api_endpoint:
                if storage.exists("spotter.json"):
                    storage_configuration_json = storage.read_json("spotter.json")
                    api_endpoint = storage_configuration_json.get("endpoint", ApiClient.DEFAULT_ENDPOINT)
                else:
                    api_endpoint = ApiClient.DEFAULT_ENDPOINT

            api_client = ApiClient(api_endpoint, storage, api_token, username, password, debug=debug)
            api_client.debug_print_me()

            progress.update(progress_task, description="Scanning...", total=None)
            if project_id:
                api_client.debug_print("Scanning with project id {}", project_id)
                api_client.debug_project(project_id)
                scan_start_time = time.time()
                response_scan_async = api_client.post(
                    f"/v3/scans_async/?project={project_id}",
                    payload=compat_to_jsonable_python(scan_payload),
                    timeout=120,
                )
            else:
                api_client.debug_print("Scanning with default organization and project")
                api_client.debug_my_default_organization()
                scan_start_time = time.time()
                response_scan_async = api_client.post(
                    "/v3/scans_async/", payload=compat_to_jsonable_python(scan_payload), timeout=120
                )

            try:
                response_scan_start_json = response_scan_async.json()
                scan_start_async = StartAsync.from_api_response(response_scan_start_json)
                scan_progress = scan_start_async.scan_progress
                progress.update(progress_task, description=f"Scanning ({scan_progress.progress_status})...", total=None)

                response_scan_result_json = {}
                ending_statuses = [s.value for s in ScanProgressStatus if s.value > 1]
                while scan_progress.progress_status.value not in ending_statuses:
                    response_scan = api_client.get(f"/v3/scans/{scan_start_async.uuid}", timeout=120)
                    response_scan_result_json = response_scan.json()
                    scan_progress = ScanProgress.from_api_response_element(
                        response_scan_result_json.get("scan_progress", None)
                    )
                    if scan_progress.progress_status.value > 0:
                        progress.update(
                            progress_task,
                            description=f"Scanning ({scan_progress.progress_status})...",
                            completed=scan_progress.current,
                            total=scan_progress.total,
                        )
                    time.sleep(0.5)

                scan_time = time.time() - scan_start_time
            except json.JSONDecodeError as e:
                print(f"Error: error when converting to JSON: {str(e)}", file=sys.stderr)
                sys.exit(2)

            if scan_progress.progress_status == ScanProgressStatus.SUCCESS:
                progress_custom_theme.styles["progress.percentage"] = Style(color="rgb(86,194,133)")
            else:
                progress_custom_theme.styles["bar.finished"] = Style(color="rgb(249,78,112)")
                progress_custom_theme.styles["progress.percentage"] = Style(color="rgb(249,78,112)")

            progress.console.use_theme(progress_custom_theme)
            progress.update(progress_task, description=f"Scanning...{scan_progress.progress_status}.")
            progress.stop()
            if not no_progress:
                print()

            scan_result = Result.from_api_response(
                response_scan_result_json, parsing_result.tasks, parsing_result.playbooks, scan_time
            )

            # we have to do rewrite before any filtering and sorting to keep original order of check results
            if rewrite:
                scan_result.apply_check_result_suggestions(scan_paths, display_level)

            # TODO: figure out if we can filter and/or sort returned check results on the backend
            scan_result.filter_check_results(display_level)
            scan_result.sort_check_results()

            try:
                formatted_output = scan_result.format_output(output_format, no_colors, no_docs_url, rewrite)
                if output_path:
                    output_path.write_text(formatted_output, encoding="utf-8")
                    print(f"Scan result exported to {output_path}.", file=sys.stderr)
                else:
                    print(formatted_output)

                if junit_xml:
                    junit_xml_string = scan_result.format_junit_xml(no_docs_url)
                    junit_xml.write_text(junit_xml_string, encoding="utf-8")
                    print(f"JUnitXML report saved to {junit_xml}.", file=sys.stderr)
            except TypeError as e:
                print(f"Error: {str(e)}", file=sys.stderr)
                sys.exit(2)

            if len(scan_result.check_results) > 0:
                sys.exit(1)
