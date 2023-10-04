"""Provide utility functions that can be used as helpers throughout the code."""

import argparse
import sys
from typing import Optional, cast
from urllib.parse import urlparse

if sys.version_info >= (3, 8):
    from importlib.metadata import distribution as get_distribution, PackageNotFoundError as TestError
else:
    from pkg_resources import get_distribution, DistributionNotFound as TestError


def get_package_version(package: str, throw: bool) -> Optional[str]:
    """
    Retrieve current version of Python package.

    :return: Version string
    """
    try:
        return get_distribution(package).version
    except TestError as e:
        if throw:
            print(f"Error: retrieving current {package} version failed: {e}", file=sys.stderr)
            sys.exit(2)
    return None


def get_current_cli_version() -> str:
    """
    Retrieve current version of Steampunk Spotter CLI (steampunk-spotter Python package).

    :return: Version string
    """
    version = get_package_version("steampunk-spotter", True)
    return cast(str, version)


def validate_url(url: str) -> str:
    """
    Validate URL.

    :param url: URL to validate
    :return: The same URL as input
    """
    parsed_url = urlparse(url)
    supported_url_schemes = ("http", "https")
    if parsed_url.scheme not in supported_url_schemes:
        raise argparse.ArgumentTypeError(
            f"URL '{url}' has an invalid URL scheme '{parsed_url.scheme}', "
            f"supported are: {', '.join(supported_url_schemes)}."
        )

    if len(url) > 2048:
        raise argparse.ArgumentTypeError(f"URL '{url}' exceeds maximum length of 2048 characters.")

    if not parsed_url.netloc:
        raise argparse.ArgumentTypeError(f"No URL domain specified in '{url}'.")

    return url
