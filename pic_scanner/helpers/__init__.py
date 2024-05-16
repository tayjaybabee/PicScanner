import os
from pathlib import Path

from typing import Union
from warnings import warn
from .filesystem import provision_path, check_directory
from ..common.constants import IMAGE_EXTENSIONS

excluded = []

def get_picture_files(
        directory: Union[str, Path],
        recursive: bool = False,
        do_not_provision: bool = False,
        exclude_dir_names: list[str] = None,
        **kwargs) -> list:
    files = []

    if not do_not_provision:
        directory = provision_path(directory, **kwargs)

    if not check_directory(directory, do_not_provision=do_not_provision, **kwargs):
        warn(f"Invalid directory: {directory}!")
    else:
        if recursive:
            for root, _, filenames in os.walk(directory):
                if exclude_dir_names:
                    if not any([exclude_dir_name.lower() in root.lower() for exclude_dir_name in exclude_dir_names]):
                        for filename in filenames:
                            if Path(filename).suffix.lower() in IMAGE_EXTENSIONS:
                                files.append(Path(root) / filename)
                    else:
                        excluded.append(root)
                else:
                    for filename in filenames:
                        if Path(filename).suffix.lower() in IMAGE_EXTENSIONS:
                            files.append(Path(root) / filename)

        else:
            for file in directory.iterdir():
                if file.suffix.lower() in IMAGE_EXTENSIONS:
                    files.append(file)

    return files
