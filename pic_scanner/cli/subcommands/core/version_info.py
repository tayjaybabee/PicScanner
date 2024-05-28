"""
pic_scanner.cli.subcommands.core.version_info

This module contains the version info subcommand handler.

Since:
    1.0.0
"""
from pic_scanner.cli.subcommands.registry import REGISTRY
from rich.console import Console
import requests
from packaging.version import Version, InvalidVersion


CONSOLE = Console()


def check_pypi_package_version(package_name, include_prereleases=False):
    """
    Check if a package is available on PyPi and retrieve its latest version.

    Args:
        package_name (str): The name of the package to check.
        include_prereleases (bool): Whether to include pre-releases in the version check.

    Returns:
        str: The latest version of the package if it exists, otherwise None.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        versions = data.get('releases', {}).keys()

        def is_stable_version(version):
            try:
                v = Version(version)
                return not v.is_prerelease
            except InvalidVersion:
                return False

        if not include_prereleases:
            versions = [v for v in versions if is_stable_version(v)]

        if versions:
            try:
                return str(max(Version(v) for v in versions))
            except InvalidVersion:
                return None
        else:
            return None
    elif response.status_code == 404:
        print(f"Package '{package_name}' not found on PyPi.")
        return None
    else:
        print(f"Failed to fetch package info for '{package_name}'. HTTP Status Code: {response.status_code}")
        return None


def handle_version_info(args):
    if args.version_info == 'update':
        CONSOLE.print('Checking latest version info...')
