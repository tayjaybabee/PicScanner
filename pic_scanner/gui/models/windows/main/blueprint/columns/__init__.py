from pathlib import Path
from typing import Union

from inspyre_toolbox.syntactic_sweets.properties import validate_path

from pic_scanner.gui.models.element_bases import GUIFileCollection
from pic_scanner.gui.models.element_bases.column import Column, psg
from pic_scanner.helpers.filesystem.classes import FileCollection
from pic_scanner.helpers.images import get_image_data
from pic_scanner.helpers.locks import flag_lock

from pic_scanner.gui.models.element_bases.button import ButtonSchematic
from pic_scanner.gui.models.element_bases.button.factories import ButtonFactory, GUIElementKeyFactory

gui_file_collection = None


class LeftColumn(Column):
    """
    A class that represents the left column of the main window.

    Properties:
        file_collection (FileCollection):
            The collection of files.

        file_list_box (psg.Listbox):
            The listbox displaying the file names.

        file_names (list[str]):
            The list of file names.

        next_button (psg.Button):
            The button to go to the next file.

        file_num_display_elem (psg.Text):
            The element displaying the current file number.

        prev_button (psg.Button):
            The button to go to the previous file.

        remove_button (psg.Button):
            The button to remove the current image.
    """
    instances = []

    def __init__(self, file_collection: FileCollection, **kwargs):
        """
        Initializes the LeftColumn with a given FileCollection.

        Parameters:

            file_collection (FileCollection):
                The collection of files.

            **kwargs:
                Additional keyword arguments.

        Raises:
            TypeError: If the `file_collection` attribute is not an instance of FileCollection.
        """
        global gui_file_collection

        if not isinstance(file_collection, FileCollection):
            raise TypeError('The `file_collection` attribute must be of type `FileCollection`.')

        self.__file_collection = file_collection

        if not gui_file_collection:
            gui_file_collection = GUIFileCollection(file_collection)

        super().__init__('LEFT_COLUMN', **kwargs)

        self.__file_list_box = None
        self.__file_num_display_elem = None

        self.__button_factory = ButtonFactory('main window')

        self.__next_button = None

        self.__prev_button = None
        self.__remove_button = None

        self.instances.append(self)

    @property
    def 

    @property
    def file_collection(self):
        """
        Gets the file collection.

        Returns:
            FileCollection:
                The collection of files.
        """
        return self.__file_collection

    @property
    def file_list_box(self):
        """
        Gets the file list box.

        Returns:
            psg.Listbox:
                The listbox displaying the file names.
        """
        if self.building and not self.is_built and self.file_collection is not None and self.__file_list_box is None:
            print('Creating file listbox')

            self.__file_list_box = psg.Listbox(
                self.file_names,
                size=(80, 20),
                key='FILE_LIST_BOX',
                enable_events=True,
            )
        return self.__file_list_box

    @property
    def file_names(self):
        """
        Gets the file names.

        Returns:
            list[str]:
                The list of file names.

        """
        return self.file_collection.paths

    @property
    def next_button(self):
        """
        Gets the next button.


        Returns:
            psg.Button:
                The button to go to the next file.

        """
        if self.building and not self.is_built and self.__next_button is None:

            self.__next_button = self.
        return self.__next_button

    @property
    def file_num_display_elem(self):
        """
        Gets the file number display element.

        Returns:
            psg.Text:
                The element displaying the current file number.
        """
        if self.building and not self.is_built and self.file_collection is not None and self.__file_num_display_elem is None:
            self.__file_num_display_elem = psg.Text(
                f'File 1 of {self.file_collection.total_files}',
                size=(30, 2),
                key='FILE_NUM_DISPLAY'
            )
        return self.__file_num_display_elem

    @property
    def prev_button(self):
        """
        Gets the previous button.

        Returns:
            psg.Button:
                The button to go to the previous file.

        """

        if self.building and not self.is_built and self.__prev_button is None:
            self.__prev_button = ButtonSchematic(
                    'Previous file',
                    create_disabled=True,
                    auto_build=True
                    )
        return self.__prev_button

    @property
    def remove_button(self):
        """
        Gets the remove button.

        Returns:
            psg.Button:
                The button to remove the current image.
        """
        if self.building and not self.is_built and self.__remove_button is None:
            self.__remove_button = ButtonSchematic(
                    'Remove file',
                    create_disabled=True,
                    auto_build=True
                    )
        return self.__remove_button

    def build(self):
        """
        Builds the left column layout.

        Returns:
            psg.Column: The column layout.
        """


        print(
            f"Starting build: is_built={self.is_built}, file_collection is not None={self.file_collection is not None}, building={self.building}")  # Debugging
        if not self.is_built and self.file_collection is not None and not self.building:
            with flag_lock(self, 'building'):
                print("Inside flag_lock")  # Debugging
                self._layout = [
                        [self.file_list_box],
                        [
                                self.next_button.button,
                                self.prev_button.button,
                                self.remove_button.button

                                ]
                        ]
                self._column = psg.Column(self.layout, key='LEFT_COLUMN')
                self._built = True
                print("Build complete")  # Debugging

        return self.column



class FileColumn(Column):

    def __init__(self, file_path, **kwargs):
        global gui_file_collection

        if not LeftColumn.instances:
            raise AttributeError('The `LeftColumn` class has not been instantiated yet.')

        super().__init__('FILE_COLUMN', **kwargs)

        self._changing_image = False

        self.__file_path = False

        self.file_path = file_path
        self.__image_elem = None
        self.__file_name_display_elem = None

    @property
    def building(self) -> bool:
        return self._building

    @property
    def changing_image(self) -> bool:
        return self._changing_image

    @property
    def file_name_display_elem(self) -> psg.Text:
        if self.building and (not self.is_built and self.__file_name_display_elem is None):
            self.__file_name_display_elem = psg.Text(
                    self.file_path.name,
                    size=(80, 3),
                    key='FILE_NAME_DISPLAY'
                    )

        if not self.building and not self.is_built:
            raise AttributeError('The file name display element has not been built yet.')

        return self.__file_name_display_elem

    @property
    def file_path(self) -> Path:
        """
        A property that returns the file path.

        Returns:
            Path:
        """
        return self.__file_path

    @file_path.setter
    @validate_path(exists=True)
    def file_path(self, new) -> None:
        if self.is_built and new != self.__file_path:
            self.__needs_update = True
            self.__file_path = new

        if self.is_built and new != self.__file_path and not self.changing_image:
            self.change_image(new)

        self.__file_path = new

    @property
    def gui_file_collection(self):
        global gui_file_collection

        return gui_file_collection

    @property
    def image_elem(self) -> psg.Image:
        """
        A property that returns the image element.

        Returns:
            The image element.
        """

        if self.building and not self.is_built:
            self.__image_elem = psg.Image(
                    data=get_image_data(
                            str(self.file_path,),
                            maxsize=(800, 800)),
                    key='IMAGE_DISPLAY',
                    )

        if not self.building and not self.is_built:
            raise AttributeError('The image element has not been built yet.')

        return self.__image_elem

    def build(self) -> psg.Column:
        """
        Builds the column.

        This method builds the column by creating the layout and column elements and setting the
        `is_built ` attribute to `True`.

        Returns:
            The column.
        """
        if not self.is_built and self.file_path is not None:

            with flag_lock(self, 'building'):
                self._layout = [
                        [self.file_name_display_elem],
                        [self.image_elem]
                        ]

                self._column = psg.Column(self.layout, key='FILE_COLUMN')

                if self.gui_file_collection is not None and isinstance(self.gui_file_collection, GUIFileCollection):
                    self.gui_file_collection.add_cursor_callback(self.change_image)

        self._built = True

        return self.column

    def change_image(self, new_path: Union[Path, str, int]) -> None:
        """
        Changes the image displayed in the column.

        This method changes the image displayed in the column to the image located at the path and
        updates the file name display element to show the new file name.

        Parameters:
              new_path (Path):
                    The new path to the image.
        """
        if not self.is_built:
            raise AttributeError('The column has not been built yet.')

        if isinstance(new_path, int):
            new_path = self.gui_file_collection[new_path]

        with flag_lock(self, 'changing_image'):
            self.file_path = new_path
            self.image_elem.update(data=get_image_data(str(self.file_path)))
            self.file_name_display_elem.update(value=self.file_path.name)
