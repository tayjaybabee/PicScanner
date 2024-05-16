from dataclasses import dataclass, field

from . import check_file, provision_paths
from .units import UNIT_MAP

from pathlib import Path
from typing import Union

from inspyre_toolbox.conversions.bytes import ByteConverter
from inspyre_toolbox.humanize import Numerical


# Create a data class that takes a collection of file paths and creates a class representing a
# collection of files with properties for total size and number of files and a dictionary of extensions with
# properties for total size and number of files.


def get_lowest_unit_size(size: int) -> tuple[Union[int, float], str]:
    """
    Get the lowest unit size for a given size.

    Parameters:
        size (int):
            The size to convert.

    Returns:
        tuple[Union[int, float], str]:
            The converted size and the unit.

    Examples:
        >>> get_lowest_unit_size(1024)
        (1.0, 'KB')
        >>> get_lowest_unit_size(1024 * 1024)
        (1.0, 'MB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024)
        (1.0, 'GB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024)
        (1.0, 'TB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024 * 1024)
        (1.0, 'PB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024 * 1024 * 1024)
        (1.0, 'EB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024)
        (1.0, 'ZB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024)
        (1.0, 'YB')
    """
    units = ['byte', 'kilobyte', 'megabyte', 'gigabyte', 'terabyte', 'petabyte', 'exabyte', 'zetabyte', 'yottabyte']
    units.reverse()
    converter = ByteConverter(size, 'byte')

    for unit in units:
        converted = converter.convert(unit.lower())

        if converted >= 1:
            return converted, unit.upper(),


@dataclass
class FileCollection:
    paths: list
    total_size: int = field(init=False, default=0)
    total_files: int = field(init=False, default=0)
    extensions: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        self._process_files()

    def _process_files(self):
        self.paths = provision_paths(self.paths)
        for path_str in self.paths:
            path = Path(path_str)
            if check_file(path, do_not_provision=True):
                extension = path.suffix

                if extension not in self.extensions:
                    self.extensions[extension] = {
                            'total_size':  0,
                            'total_files': 0,
                            }

                file_size = path.stat().st_size
                self.total_size += file_size
                self.total_files += 1

                self.extensions[extension]['total_size'] += file_size
                self.extensions[extension]['total_files'] += 1

    def get_total_size_in_lowest_unit(self) -> tuple[Union[int, float], str]:
        return get_lowest_unit_size(self.total_size)

    def get_total_extension_size_in_lowest_unit(
            self,
            extension: str,
            return_as_string: bool = False
            ) -> tuple[Union[int, float], str]:

        if not extension.startswith('.'):
            extension = f".{extension}"

        extension = extension.lower()

        if extension not in self.extensions:
            raise ValueError(f"Invalid extension: {extension}!")

        lowest_unit_size = get_lowest_unit_size(self.extensions[extension]['total_size'])

        if return_as_string:
            size_str = Numerical(lowest_unit_size[0], noun=lowest_unit_size[1]).count_noun()
            return size_str

        return lowest_unit_size

    def __str__(self):
        size, unit = self.get_total_size_in_lowest_unit()

        size_str = Numerical(size, noun=unit).count_noun()

        return f"Total size: {size_str}, Total files: {self.total_files}"
