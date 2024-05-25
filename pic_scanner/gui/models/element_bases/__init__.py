from pic_scanner.helpers.filesystem.classes import FileCollection
from pic_scanner.helpers.properties import ReactiveProperty


class GUIFileCollection:
    """
    A class to manage a collection of files with a cursor to navigate through them.

    Attributes:
        collection (FileCollection): The collection of files.
        __files (list[Path]): List of file paths from the collection.
        cursor (int): Current position of the cursor in the collection.
    """
    cursor = ReactiveProperty(0)

    def __init__(self, collection: FileCollection):
        """
        Initializes the GUIFileCollection with a given FileCollection.

        Args:
            collection (FileCollection): The file collection to manage.

        Raises:
            TypeError: If the collection is not an instance of FileCollection.
        """
        if not isinstance(collection, FileCollection):
            raise TypeError('The `collection` attribute must be of type `FileCollection`.')

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

    def next(self) -> str:
        """
        Moves the cursor to the next file in the collection and returns it.

        Returns:
            str: The path of the next file.
        """
        if self.cursor < len(self.__files) - 1:
            self.cursor += 1
        return self.__files[self.cursor]

    def prev(self) -> str:
        """
        Moves the cursor to the previous file in the collection and returns it.

        Returns:
            str: The path of the previous file.
        """
        if self.cursor > 0:
            self.cursor -= 1
        return self.__files[self.cursor]

    def current(self) -> str:
        """
        Returns the file at the current cursor position.

        Returns:
            str: The path of the current file.
        """
        return self.__files[self.cursor]

    def set_cursor(self, index: int):
        """
        Sets the cursor to the specified index, adjusting if out of bounds.

        Args:
            index (int): The position to set the cursor to.

        Raises:
            IndexError: If the index is out of the valid range.
        """
        if index < 0 or index >= len(self.__files):
            raise IndexError('Cursor index out of range.')
        self.cursor = index

    def __getitem__(self, key: int) -> str:
        """
        Returns the file at the specified index.

        Args:
            key (int): The index of the file to retrieve.

        Returns:
            str: The path of the file at the specified index.
        """
        return self.__files[key]

    def add_cursor_callback(self, callback, *args, **kwargs):
        """
        Adds a callback to be invoked when the cursor changes.

        Args:
            callback (callable): The callback function.
            *args: Additional positional arguments to pass to the callback.
            **kwargs: Additional keyword arguments to pass to the callback.
        """
        self.__class__.cursor.add_callback(callback, *args, **kwargs)

    def __len__(self) -> int:
        """
        Returns the number of files in the collection.

        Returns:
            int: The number of files.
        """
        return len(self.__files)
