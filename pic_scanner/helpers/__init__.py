import inspect
import os
from pathlib import Path

from typing import Union
from warnings import warn

from pic_scanner.common.constants import IMAGE_EXTENSIONS
from pic_scanner.log_engine import MAIN_MOD_LOGGER

MOD_LOGGER = MAIN_MOD_LOGGER.get_child('helpers')


excluded = []


def is_class(obj):
    """
    Determine if an object is a class.

    Parameters:
        obj:
            The object to check.

    Returns:
        bool:
            True if the object is a class; False otherwise.

    Example:
        >>> is_class(str)
        True
        >>> is_class('string')
        False
    """
    return inspect.isclass(obj)


def is_instance(obj):
    """
    Determine if an object is an instance of a class.

    Parameters:
         obj:
             The object to check.

    Returns:
        bool:
            True if the object is an instance of a class; False otherwise.

    Example:
        >>> is_instance(str)
        False
        >>> is_instance('string')
        True
    """
    return not is_class(obj)


def get_picture_files(
        directory: Union[str, Path],
        recursive: bool = False,
        do_not_provision: bool = False,
        exclude_dir_names: list[str] = None,
        **kwargs) -> list:
    """
    Get a list of picture files in a directory.

    This function searches a directory for picture files and returns a list
    of the picture files found. The search can be performed recursively
    and specific directories can be excluded from the search.

    Note:
        Use of the `exclude_dir_names` parameter is case-insensitive, and
        directory-depth is not considered when excluding directories. **If
        a nested directory contains an excluded directory name, the nested
        directory will be excluded.**

    Parameters:
        directory (str or Path):
            The directory to search for picture files.

        recursive (bool):
            A flag indicating whether to search recursively.

        do_not_provision (bool):
            A flag indicating whether to provision the directory.

        exclude_dir_names (list):
            A list of directory names to exclude.

        **kwargs:
            Additional keyword arguments.

    Returns:
        list[Path]:
            A list of picture files in the directory.

    Example:
        >>> get_picture_files('path/to/directory', recursive=True)
        [Path('path/to/directory/image1.jpg'), Path('path/to/directory/image2.jpg')]
    """
    from pic_scanner.helpers.filesystem import provision_path, check_directory

    files = []

    if not do_not_provision:
        directory = provision_path(directory, **kwargs)

    if not check_directory(directory, do_not_provision=do_not_provision, **kwargs):
        warn(f"Invalid directory: {directory}!")
    elif recursive:
        for root, _, filenames in os.walk(directory):
            if exclude_dir_names:
                if all(
                    exclude_dir_name.lower() not in root.lower()
                    for exclude_dir_name in exclude_dir_names
                        ):
                    files.extend(
                        Path(root) / filename
                        for filename in filenames
                        if Path(filename).suffix.lower()
                        in IMAGE_EXTENSIONS
                            )
                else:
                    excluded.append(root)
            else:
                files.extend(
                    Path(root) / filename
                    for filename in filenames
                    if Path(filename).suffix.lower() in IMAGE_EXTENSIONS
                        )
    else:
        files.extend(
            file
            for file in directory.iterdir()
            if file.suffix.lower() in IMAGE_EXTENSIONS
                )
    return files


def get_file_collection(
        directory: Union[str, Path],
        recursive: bool = False,
        do_not_provision: bool = False,
        exclude_dir_names: list[str] = None,
        **kwargs) -> 'FileCollection':
    """
    Get a FileCollection object for a directory.

    This function searches a directory for picture files and returns a
    FileCollection object containing the picture files found. The search
    can be performed recursively and specific directories can be excluded
    from the search.

    Note:
        Use of the `exclude_dir_names` parameter is case-insensitive, and
        directory-depth is not considered when excluding directories. **If
        a nested directory contains an excluded directory name, the nested
        directory will be excluded.**

    Parameters:
        directory (str or Path):
            The directory to search for picture files.

        recursive (bool):
            A flag indicating whether to search recursively.

        do_not_provision (bool):
            A flag indicating whether to provision the directory.

        exclude_dir_names (list):
            A list of directory names to exclude.

        **kwargs:
            Additional keyword arguments.

    Returns:
        FileCollection:
            A FileCollection object containing the picture files in the directory.

    Example:
        >>> get_file_collection('path/to/directory', recursive=True)
        FileCollection(paths=[Path('path/to/directory/image1.jpg'), Path('path/to/directory/image2.jpg')])
    """
    from pic_scanner.helpers.filesystem.classes import FileCollection

    return FileCollection(
        get_picture_files(
            directory,
            recursive=recursive,
            do_not_provision=do_not_provision,
            exclude_dir_names=exclude_dir_names,
            **kwargs
            )
        )


def get_caller_name():
    """
    Get the name of the calling function.

    Returns:
        str:
            The name of the calling function.

    Example:
        >>> get_caller_name()
        'get_caller_name'
    """
    return inspect.stack()[2].function
