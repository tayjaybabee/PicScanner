from pathlib import Path
from typing import Union


__all__ = [
    'check_path',
    'check_directory',
    'check_file',
    'provision_path',


]


def check_path(
        path: Union[str, Path],
        do_not_expand: bool = False,
        do_not_resolve: bool = False,
        do_not_convert: bool = False,
        do_not_provision: bool = False,
) -> bool:
    """
    Check if a path is valid.

    Parameters:
        path (Union[str, Path]):
            The path to check.

        do_not_expand (bool):
            A flag indicating whether to expand the path.

        do_not_resolve (bool):
            A flag indicating whether to resolve the path.

        do_not_convert (bool):
            A flag indicating whether to convert the path to a string.

        do_not_provision (bool):
            A flag indicating whether to provision the path.

    Returns:
        bool:
            A flag indicating whether the path is valid.
    """
    if not do_not_provision:
        path = provision_path(
            path,
            do_not_convert=do_not_convert,
            do_not_expand=do_not_expand,
            do_not_resolve=do_not_resolve
        )

    if not isinstance(path, Path):
        return False

    return path.exists()


def check_directory(
        path: Union[str, Path],
        **kwargs
) -> bool:
    """
    Check if a directory is valid.

    Parameters:
        path (Union[str, Path]):
            The directory to check.

    Returns:
        bool:
            A flag indicating whether the directory is valid.
    """
    if check_path(path, **kwargs):
        return path.is_dir()
    else:
        return False


def check_file(
        path: Union[str, Path],
        **kwargs
) -> bool:
    """
    Check if a file is valid.

    Parameters:
        path (Union[str, Path]):
            The file to check.

    Returns:
        bool:
            A flag indicating whether the file is valid.
    """
    if check_path(path, **kwargs):
        return path.is_file()
    else:
        return False


def provision_path(
        path: Union[str, Path],
        do_not_expand: bool = False,
        do_not_resolve: bool = False,
        do_not_convert: bool = False,
) -> Path:
    """
    Provision a path.

    Parameters:
        path (str):
            The path to provision.

        do_not_convert (bool):
            A flag indicating whether to convert the path to a string.

        do_not_expand (bool):
            A flag indicating whether to expand the path.

        do_not_resolve (bool):
            A flag indicating whether to resolve the path.

    Returns:
        Path:
            The provisioned path.
    """
    if not isinstance(path, Path):
        if isinstance(path, str) and not do_not_convert:
            path = Path(path)
        else:
            raise ValueError(f"Invalid path: {path}!")

    if not do_not_expand:
        path = path.expanduser()

    if not do_not_resolve:
        path = path.resolve()

    return path


def provision_paths(path_list: list) -> list:
    """
    Provision a list of paths.

    Parameters:
        path_list (list):
            The list of paths to provision.

    Returns:
        list:
            The provisioned list of paths.
    """
    return [provision_path(path) for path in path_list]


def gather_files_in_dir(
        directory: Union[str, Path],
        recursive: bool = False,
        file_types: Union[str, list] = None,
        **kwargs
) -> list:
    """
    Gather all files in a directory.

    Parameters:
        directory (Union[str, Path]):
            The directory to gather files from.

        recursive (bool):
            A flag indicating whether to gather files recursively.

        file_types (Union[str, list]):
            The file types to gather.

    Returns:
        list:
            A list of files in the directory.
    """
    directory = provision_path(directory)

    if not check_directory(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not file_types:
        file_types = ['*']

    if isinstance(file_types, str):
        file_types = [file_types]

    files = []

    for file_type in file_types:
        files.extend(directory.glob(f'**/*.{file_type}'))

    return files


def get_storage_unit_abbreviation(unit):
    """
    Get the abbreviation for a storage unit.

    Parameters:
        unit (str):
            The storage unit.

    Returns:
        str:
            The abbreviation for the storage unit.
    """
    return {
        'byte': 'B',
        'kilobyte': 'KB',
        'megabyte': 'MB',
        'gigabyte': 'GB',
        'terabyte': 'TB',
        'petabyte': 'PB',
        'exabyte': 'EB',
        'zetabyte': 'ZB',
        'yottabyte': 'YB'
    }.get(unit, 'B')
