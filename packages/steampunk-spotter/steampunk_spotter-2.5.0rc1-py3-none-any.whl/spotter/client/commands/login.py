"""Provide login CLI command."""

import argparse
import os
from getpass import getpass
from pathlib import Path
from typing import Optional

from spotter.library.api import ApiClient
from spotter.library.storage import Storage


def add_parser(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    """
    Add a new parser for login command to subparsers.

    :param subparsers: Subparsers action
    """
    parser = subparsers.add_parser(
        "login", help="Log in to Steampunk Spotter user account", description="Log in to Steampunk Spotter user account"
    )
    parser.set_defaults(func=_parser_callback)


def _parser_callback(args: argparse.Namespace) -> None:
    """
    Execute callback for login command.

    :param args: Argparse arguments
    """
    api_endpoint = args.endpoint or os.environ.get("SPOTTER_ENDPOINT", "")
    storage_path = args.storage_path or Storage.DEFAULT_PATH
    api_token = args.api_token or os.environ.get("SPOTTER_API_TOKEN")
    username = args.username or os.environ.get("SPOTTER_USERNAME")
    password = args.password or os.environ.get("SPOTTER_PASSWORD")
    if not api_token and not username:
        username = input("Username: ")
    if not api_token and not password:
        password = getpass()

    login(api_endpoint, storage_path, api_token, username, password, debug=args.debug)
    print("Login successful!")


def login(
    api_endpoint: str,
    storage_path: Path,
    api_token: Optional[str],
    username: Optional[str],
    password: Optional[str],
    debug: bool = False,
) -> None:
    """
    Do user login.

    :param api_endpoint: Steampunk Spotter API endpoint
    :param storage_path: Path to storage
    :param api_token: Steampunk Spotter API token
    :param username: Steampunk Spotter username
    :param password: Steampunk Spotter password
    :param debug: Enable or disable debug mode
    """
    storage = Storage(storage_path)

    # TODO: extract this to a separate configuration component along with other configuration file options
    if not api_endpoint:
        if storage.exists("spotter.json"):
            storage_configuration_json = storage.read_json("spotter.json")
            api_endpoint = storage_configuration_json.get("endpoint", ApiClient.DEFAULT_ENDPOINT)
        else:
            api_endpoint = ApiClient.DEFAULT_ENDPOINT

    api_client = ApiClient(api_endpoint, storage, api_token, username, password, debug=debug)
    api_client.login()
