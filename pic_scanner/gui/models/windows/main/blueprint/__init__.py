from inspyre_toolbox.syntactic_sweets.properties import RestrictedSetter

from pic_scanner.helpers.locks import flag_lock
from pic_scanner.helpers.filesystem.classes import FileCollection
from .columns import LeftColumn, FileColumn
from pic_scanner.gui.models.element_bases.blueprint import BaseBlueprint
from pic_scanner.gui.models.element_bases import GUIFileCollection

from pic_scanner.gui.models.windows.main import MOD_LOGGER as PARENT_LOGGER
from pic_scanner.log_engine import Loggable


MOD_LOGGER = PARENT_LOGGER.get_child('blueprint')


class BluePrint(BaseBlueprint, Loggable):

    __left_column = RestrictedSetter(
            'left_column',
            initial=None,
            allowed_types=(LeftColumn,),

            )

    __file_column = RestrictedSetter(
            'file_column',
            initial=None,
            allowed_types=(FileColumn,),

            )

    __file_collection_cursor = RestrictedSetter(
            'file_collection_cursor',
            initial=None,
            allowed_types=GUIFileCollection,
            restrict_setter=True
            )

    def __init__(
            self,
            file_collection: "pic_scanner.helpers.filesystem.classes.FileCollection",
            pre_built_left_column=None,
            pre_built_file_column=None,
            **kwargs

            ):
        if not isinstance(file_collection, FileCollection):
            raise TypeError('The `file_collection` attribute must be of type `FileCollection`.')

        Loggable.__init__(self, parent_log_device=MOD_LOGGER)
        BaseBlueprint.__init__(self, **kwargs)

        self.__file_collection = file_collection

        self.log_device.debug(
                f'Received a collection with {file_collection.total_files} files. With the following extensions '
                f'represented: {", ".join(list(file_collection.extensions.keys()))}'
            )

        self.__file_collection_cursor = GUIFileCollection(file_collection)

        self.log_device.debug(
                f'Created a file collection cursor with {file_collection.total_files} files. With the following '
                f'extensions represented: {", ".join(list(file_collection.extensions.keys()))}'
            )

        if pre_built_left_column and isinstance(pre_built_left_column, LeftColumn):

            self.log_device.debug('Using pre-built left column')
            self.__left_column = pre_built_left_column
        else:
            self.log_device.debug('Building left column')
            self.__left_column = LeftColumn(self.file_collection, **kwargs)

        if pre_built_file_column and isinstance(pre_built_file_column, FileColumn):
            self.log_device.debug('Using pre-built file column')
            self.__file_column = pre_built_file_column
        else:
            self.log_device.debug('Building file column')
            self.__file_column = FileColumn(self.file_collection[0], **kwargs)

        self._building     = False
        self.__layout      = []

    @property
    def building(self):
        return self._building

    @building.deleter
    def building(self):
        self._building = False

    @property
    def file_collection(self):
        return self.__file_collection

    @property
    def file_collection_cursor(self):
        return self.__file_collection_cursor


    @property
    def file_column(self):
        """
        A property that returns the file column.

        The file column is the column that displays the image in the GUI representation of the blueprint. This is the
        right column in the blueprint layout. This property is a RestrictedSetter, and can only be set to an instance of
        FileColumn. The initial value is None.

        Returns:
            FileColumn:
                The file column.
        """
        return self.__file_column


    @property
    def left_column(self):
        """
        A property that returns the left column.

        Returns:
            LeftColumn:
                The left column.
        """
        return self.__left_column

    def build(self):
        """
        Build the blueprint layout.

        Returns:
            list:
                The layout of the blueprint.
        """

        if not self.is_built:
            with flag_lock(self, 'building'):
                parts = [self.left_column, self.file_column]

                built_parts = []

                for part in parts:
                    if not part.is_built:
                        part.build()
                    built_parts.append(part.column)

                self._layout = [
                        built_parts
                        ]

            self._built = True

        return self.layout

    def change_image(self, new_image):
        """
        Change the image in the file column.

        This method changes the image in the image element of the file column to the new image provided. The new image
        must be a path to an image file. This method is used to change the image displayed in the GUI when the user
        navigates through the images in the file collection. This method is called by the blueprint controller when the
        user changes the image.

        Parameters::
            new_image:
                The new image to display in the file column.

        Returns:
            None
        """
        self.file_column.change_image(new_image)

    def current_image(self):
        """
        Get the current image.

        This method returns the path to the current image in the file column. This is the image that is currently
        displayed in the GUI. This method is used by the blueprint controller to determine which image is currently
        displayed in the GUI. This method is called by the blueprint controller when the user changes the image. The
        blueprint controller uses this method to determine the current image. The blueprint controller then uses this
        information to update the current image in the GUI.

        Returns:
            str:
                The path to the current image.

        """
        return self.file_column.file_path

    def next_image(self):
        """
        Get the next image.

        This method moves the cursor to the next image in the file collection and returns the path to that image. This
        method is used by the blueprint controller to move the cursor to the next image in the file collection. This
        method is called by the blueprint controller when the user clicks the 'Next' button in the GUI. The blueprint
        controller uses this method to move the cursor to the next image in the file collection. The blueprint controller
        then uses this information to update the current image in the GUI.

        Returns:
            str:
                The path to the next image.

        """
        image = self.file_collection_cursor.next()

    def update_image(self):
        if self.current_image != self.file_collection_cursor.current:
            self.change_image(self.file_collection_cursor.current)
