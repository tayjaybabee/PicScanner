"""
classes.py

This module provides a class for managing a collection of files and a class for managing a single file. The FileCollection
class takes a list of file paths and creates a class representing a collection of files with properties for total size and
number of files and a dictionary of extensions with properties for total size and number of files. The File class is a
placeholder for future development. It is not currently used in the application. It is intended to be used for managing
individual files in the future.

Classes:
    File:
        A placeholder class for managing individual files.

    FileCollection:
        A class for managing a collection of files.

        Methods:
            get_total_size_in_lowest_unit:
                Get the total size of the collection in the lowest unit.

            get_total_extension_size_in_lowest_unit:
                Get the total size of a specific extension in the lowest unit.

            remove_file:
                Remove a file from the collection.

            reprocess_files:
                Reprocess the files in the collection.

    NeedsReprocessingTag:
        A descriptor class for managing the needs_reprocessing attribute of the FileCollection class.

Functions:
    get_lowest_unit_size:
        Get the lowest unit size for a given size.


Since:
    1.0
"""

from dataclasses import dataclass, field

from . import check_file, provision_paths

from pathlib import Path
from typing import Union, List, Dict

from inspyre_toolbox.conversions.bytes import ByteConverter
from inspyre_toolbox.humanize import Numerical

from pic_scanner.helpers.filesystem import provision_path


class NeedsReprocessingTag:
    def __init__(self, value: bool = False):
        self.__value = value if isinstance(value, bool) else None
        if self.__value is None:
            raise ValueError("Value must be a boolean.")

    def __get__(self, instance, owner):
        return self.__value

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise ValueError("Value must be a boolean.")
        self.__value = value



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


class File:
    def __init__(self, path: Union[str, Path]):
        self.__path = None


@dataclass
class FileCollection:
    """
    A class for managing a collection of files.

    Properties:
        paths (list):
            A list of file paths.

        total_size (int):
            The total size of the collection, in bytes.

        total_files (int):
            The total number of files in the collection.

        extensions (dict):
            A dictionary of extensions with properties for total size and number of files.

        needs_reprocessing (bool):
            A flag indicating whether the collection needs reprocessing.

    Methods:
        get_total_size_in_lowest_unit:
            Get the total size of the collection in the lowest unit.

        get_total_extension_size_in_lowest_unit:
            Get the total size of a specific extension in the lowest unit.

        remove_file:
            Remove a file from the collection.

        reprocess_files:
            Reprocess the files in the collection.

    Examples:
        >>> collection = FileCollection(paths=['/path/to/file1', '/path/to/file2'])
        >>> collection.total_size
        123456  # Total size of the collection, in bytes.
    """
    paths: list
    total_size: int = field(init=False, default=0)
    total_files: int = field(init=False, default=0)
    extensions: dict = field(init=False, default_factory=dict)

    def __init__(self, paths: List[str] = None):
        """
        Initialize the FileCollection with a list of file paths.

        `FileCollection` is a class for managing a collection of files. It takes a list of file paths and creates a class
        representing a collection of files with properties for total size and number of files and a dictionary of extensions
        with properties for total size and number of files.

        Parameters:
            paths (list):
                A list of file paths.

        Returns:
            None
        """
        self.paths = paths
        self.total_size = 0
        self.total_files = 0
        self.extensions = {}
        self.__needs_reprocessing = NeedsReprocessingTag()

    def __post_init__(self):
        """
        Post-initialization method for the FileCollection class.

        This method processes the files in the collection. It calculates the total size of the collection, the total number
        of files, and the total size of each extension in the collection. It populates the `total_size`, `total_files`, and
        `extensions` attributes of the class.

        Returns:
            None
        """
        self._process_files()

    @property
    def needs_reprocessing(self) -> bool:
        """
        Returns whether the collection needs reprocessing.

        This property returns a boolean value indicating whether the collection needs reprocessing. If the collection has
        been modified since the last processing, this property will return `True`. If the collection has not been modified,
        it will return `False`. The property is read-only.

        Returns:
            bool:
                True if the collection needs reprocessing, False otherwise.
        """
        return self.__needs_reprocessing

    @needs_reprocessing.setter
    def needs_reprocessing(self, value: bool):
        """
        Sets whether the collection needs reprocessing.

        This method sets the `needs_reprocessing` attribute of the collection. If the value is `True`, the collection will
        be reprocessed the next time it is accessed. If the value is `False`, the collection will not be reprocessed. The
        method is used to indicate that the collection has been modified and needs to be reprocessed.

        Parameters:
            value (bool):
                The value to set the `needs_reprocessing` attribute to. True if the collection needs reprocessing, False
                otherwise.

        Returns:
            None
        """
        self.__needs_reprocessing = value

    def _process_files(self):
        """
        Process the files in the collection.

        This method processes the files in the collection. It calculates the total size of the collection, the total number
        of files, and the total size of each extension in the collection. It populates the `total_size`, `total_files`, and
        `extensions` attributes of the class.

        Returns:
            None
        """
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

    def reprocess_files(self):
        """
        Reprocess the files in the collection.

        This method reprocesses the files in the collection. It recalculates the total size of the collection, the total
        number of files, and the total size of each extension in the collection. It populates the `total_size`, `total_files`,
        and `extensions` attributes of the class. This method is used to update the collection after files have been added
        or removed.

        Note:
            This method should be called after files have been added or removed from the collection. It will only reprocess
            the files if the `needs_reprocessing` attribute is set to `True`. After reprocessing, the `needs_reprocessing`
            attribute will be set to `False`.

        Returns:
            None

        """
        if self.needs_reprocessing:
            self.total_size = 0
            self.total_files = 0
            self.extensions = {}
            self._process_files()

    def get_total_size_in_lowest_unit(self) -> tuple[Union[int, float], str]:
        """
        Get the total size of the collection in the lowest unit with a size greater than or equal to 1.

        This method calculates the total size of the collection in the lowest unit with a size greater than or equal
        to 1. It returns the size and the unit as a tuple. The unit is a string representing the unit of the size.

        Returns:
            tuple[Union[int, float], str]:
                The total size of the collection and the unit.

        """
        return get_lowest_unit_size(self.total_size)

    def get_total_extension_size_in_lowest_unit(
            self,
            extension: str,
            return_as_string: bool = False
            ) -> tuple[Union[int, float], str]:
        """
        Get the total size of a specific extension in the lowest unit with a size greater than or equal to 1.

        Parameters:
            extension (str):
                The extension to get the size of.

            return_as_string (bool):
                A flag indicating whether to return the size as a string. If True, the size will be returned as a string
                with the unit. If False, the size will be returned as a tuple with the size and the unit.

        Returns:
            tuple[Union[int, float], str]:
                The total size of the extension and the unit.

        Raises:
            ValueError:
                If the extension is not found in the collection.
        """

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

    def remove_file(self, path: Union[Path, str], **kwargs):
        """
        Remove a file from the collection.

        This method removes a file from the collection. It takes a file path as an argument and removes the file from the
        collection. It then reprocesses the files in the collection to update the total size, total number of files, and
        total size of each extension.

        Note:
            This method does not delete the file from the file system. It only removes the file from the collection,
            and only if the file is in the collection. If the file is not in the collection, this method will raise a
            `KeyError`. After removing the file, the collection will be reprocessed to update the total size, total number
            of files, and total size of each extension.

        Parameters:
            path (Union[Path, str]):
                The file path to remove.

            **kwargs:
                Additional keyword arguments.

        Raises:
            KeyError:
                If the file is not in the collection.

        Returns:
            None
        """
        path = provision_path(path, **kwargs)
        if path in self.paths:
            self.paths.remove(path)
            self.needs_reprocessing = True
            self.reprocess_files()
            self.needs_reprocessing = False

    def __getitem__(self, key: Union[int, str]) -> Union[str, Dict[str, int]]:
        if isinstance(key, int):
            return str(self.paths[key])
        elif isinstance(key, str):
            if not key.startswith('.'):
                key = f".{key}"
            key = key.lower()
            if key not in self.extensions:
                raise KeyError(f"Extension {key} not found in file collection.")
            return self.extensions[key]
        else:
            raise TypeError("Key must be an integer (for path index) or a string (for extension).")

    def __str__(self):
        size, unit = self.get_total_size_in_lowest_unit()
        size_str = Numerical(size, noun=unit).count_noun()
        return f"Total size: {size_str}, Total files: {self.total_files}"
