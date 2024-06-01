import importlib.metadata as metadata
import sys

import requests
from rich.console import Console
from rich.table import Table

from pic_scanner.cli.subcommands.registry import REGISTRY


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
                v = metadata.version(version)
                return not v.is_prerelease
            except ValueError:
                return False

        if not include_prereleases:
            versions = [v for v in versions if is_stable_version(v)]

        if versions:
            try:
                return str(max(metadata.version(v) for v in versions))
            except ValueError:
                return None
        else:
            return None
    elif response.status_code == 404:
        print(f"Package '{package_name}' not found on PyPi.")
        return None
    else:
        print(f"Failed to fetch package info for '{package_name}'. HTTP Status Code: {response.status_code}")
        return None


def get_package_info(package_name):
    """
    Get version and license information for a given package.

    Args:
        package_name (str): The name of the package to check.

    Returns:
        dict: A dictionary with version and license information.
    """
    try:
        dist = metadata.distribution(package_name)
        metadata_content = dist.metadata
        license_info = metadata_content.get('License', 'Unknown')
        return {
                "version": dist.version,
                "license": license_info
                }
    except metadata.PackageNotFoundError:
        return {
                "version": "Not installed",
                "license": "Unknown"
                }


def handle_version_update(args):
    if args.version_info == 'update':
        CONSOLE.print('Checking latest version info...')

        package_name = 'pic_scanner'  # Replace with your actual package name
        if latest_version := check_pypi_package_version(
                package_name, include_prereleases=args.include_prereleases
                ):
            CONSOLE.print(f"The latest version of '{package_name}' is {latest_version}.")
        else:
            CONSOLE.print(f"Could not retrieve the latest version for '{package_name}'.")


def handle_version_info(args):
    # Gather information
    python_version = sys.version
    python_executable = sys.executable
    package_info = get_package_info('PySimpleGUI')
    latest_version = check_pypi_package_version('pic_scanner', include_prereleases=args.include_prereleases)

    # Create the table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Attribute", style="dim")
    table.add_column("Value")

    table.add_row("Version", "3.1.0-dev.4")
    table.add_row("Full Version Name", "v3.1.0 Development Build 4")
    table.add_row("Python Executable Path", python_executable)
    table.add_row("Python Version", python_version)
    table.add_row("PySimpleGUI Version", package_info['version'])
    table.add_row("PySimpleGUI License", package_info['license'])
    table.add_row("Latest Version on PyPi", latest_version or "Unknown")

    # Print the table
    CONSOLE.print(table)


REGISTRY.register_subcommand(
        name='version',
        help_text='Version information commands',
        handler=handle_version_update,
        arguments={
                'version_info':          {
                        'choices': ['update'],
                        'help':    'Version information action to perform'
                        },
                '--include-prereleases': {
                        'action': 'store_true',
                        'help':   'Include pre-releases in the version check'
                        }
                }
        )

REGISTRY.register_subcommand(
        name='info',
        help_text='Print detailed version information',
        handler=handle_version_info,
        arguments={
                '--include-prereleases': {
                        'action': 'store_true',
                        'help':   'Include pre-releases in the version check'
                        }
                }
        )
