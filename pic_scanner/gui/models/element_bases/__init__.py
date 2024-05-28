from pic_scanner.helpers.filesystem.classes import FileCollection
from pic_scanner.helpers.properties import ReactiveProperty

from pic_scanner.gui.models import MOD_LOGGER as PARENT_LOGGER
from pic_scanner.log_engine import Loggable


MOD_LOGGER = PARENT_LOGGER.get_child('element_bases')


class GUIFileCollection(Loggable):
    """
    A class to manage a collection of files with a cursor to navigate through them.

    Properties:
        collection (FileCollection):
            The collection of files.

        files (list[Path]):
            List of file paths from the collection.

        cursor (int):
            Current position of the cursor in the collection.
    """
    cursor = ReactiveProperty(0)

    def __init__(self, collection: FileCollection):
        """
        Initializes the GUIFileCollection with a given FileCollection.

        Args:
            collection (FileCollection):
                The file collection to manage.

        Raises:
            TypeError:
                If the collection is not an instance of FileCollection.
        """
        super().__init__(parent_log_device=MOD_LOGGER)

        if not isinstance(collection, FileCollection):
            raise TypeError('The `collection` attribute must be of type `FileCollection`.')

        self.log_device.debug(f'Received a collection with {collection.total_files} files. With the following '
                              f'extensions represented: {collection.extensions}')

        self.__collection = collection
        self.__files = collection.paths

    @property
    def collection(self) -> FileCollection:
        """
        Returns the collection of files.

        Returns:
            FileCollection:
                The collection of files.
        """
        return self.__collection

    @property
    def files(self) -> list:
        """
        Returns the list of file paths from the collection.

        Returns:
            list:
                The list of file paths.
        """
        return self.__files

    @property
    def needs_reprocessing(self) -> bool:
        """
        Returns whether the collection needs reprocessing.

        Returns:
            bool:
                True if the collection needs reprocessing, False otherwise.
        """
        return self.collection.needs_reprocessing

    @needs_reprocessing.setter
    def needs_reprocessing(self, new: bool):
        """
        Sets whether the collection needs reprocessing.

        Args:
            new (bool):
                The new value for the needs_reprocessing attribute.
        """
        self.collection.needs_reprocessing = new

    def next(self) -> str:
        """
        Moves the cursor to the next file in the collection and returns it.

        Returns:
            str:
                The path of the next file.
        """
        log_name = f'{self.log_device.name}:next'

        log = (
                self.log_device.find_child_by_name(log_name)[0]
            ) if self.log_device.has_child(log_name) else self.create_child_logger()

        log.debug(f'Moving to the next file in the collection: {self.cursor + 1}/{len(self.__files)}')

        if self.cursor < len(self.__files) - 1:
            self.cursor += 1
        else:
            log.warning('Cursor is at the end of the collection, cannot move to the next file.')
        return self.__files[self.cursor]

    def prev(self) -> str:
        """
        Moves the cursor to the previous file in the collection and returns it.

        Returns:
            str:
                The path of the previous file.
        """
        log_name = f'{self.log_device.name}:prev'

        log = (
                self.log_device.find_child_by_name(log_name)[0]
            ) if self.log_device.has_child(log_name) else self.create_child_logger()

        log.debug(f'Moving to the previous file in the collection: {self.cursor - 1}/{len(self.__files)}')

        if self.cursor > 0:
            self.cursor -= 1
        else:
            log.warning('Cursor is at the beginning of the collection, cannot move to the previous file.')

        return self.__files[self.cursor]

    def current(self) -> str:
        """
        Returns the file at the current cursor position.

        Returns:
            str:
                The path of the current file.
        """
        return self.__files[self.cursor]

    def remove_current(self):
        """
        Removes the file at the current cursor position.
        """
        log_name = f'{self.log_device.name}:remove_current'

        log = (
                self.log_device.find_child_by_name(log_name)[0]
            ) if self.log_device.has_child(log_name) else self.create_child_logger()

        log.debug(f'Removing file at cursor position: {self.cursor}/{len(self.__files)}')

        self.collection.remove_file(self.files[self.cursor])

        log.debug('Reprocessing files in collection.')

        if self.cursor >= len(self.__files):
            self.cursor -= 1
        else:
            self.cursor += 1

    def set_cursor(self, index: int):
        """
        Sets the cursor to the specified index, adjusting if out of bounds.

        Args:
            index (int):
                The position to set the cursor to.

        Raises:
            IndexError:
                If the index is out of the valid range.
        """
        log_name = f'{self.log_device.name}:set_cursor'

        log = (
                self.log_device.find_child_by_name(log_name)[0]
            ) if self.log_device.has_child(log_name) else self.create_child_logger()

        if index < 0 or index >= len(self.__files):
            log.warning(f'Index out of range: {index}. Setting cursor to 0.')
            raise IndexError('Cursor index out of range.')
        self.cursor = index

    def __getitem__(self, key: int) -> str:
        """
        Returns the file at the specified index.

        Args:
            key (int):
                The index of the file to retrieve.

        Returns:
            str:
                The path of the file at the specified index.
        """
        return self.__files[key]

    def add_cursor_callback(self, callback, *args, **kwargs):
        """
        Adds a callback to be invoked when the cursor changes.

        Args:
            callback (callable):
                The callback function.

            *args:
                Additional positional arguments to pass to the callback.

            **kwargs:
                Additional keyword arguments to pass to the callback.
        """

        log_name = f'{self.log_device.name}:add_cursor_callback'

        log = (
            self.log_device.find_child_by_name(log_name)[0]
            ) if self.log_device.has_child(log_name) else self.create_child_logger()

        log.debug(f'Adding cursor callback: {callback.__name__}')

        self.__class__.cursor.add_callback(callback, *args, **kwargs)

    def __len__(self) -> int:
        """
        Returns the number of files in the collection.

        Returns:
            int:
                The number of files.
        """
        return len(self.__files)
