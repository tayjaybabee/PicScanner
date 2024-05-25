from inspyre_toolbox.syntactic_sweets.properties import RestrictedSetter

from pic_scanner.helpers.locks import flag_lock
from pic_scanner.helpers.filesystem.classes import FileCollection
from .columns import LeftColumn, FileColumn
from pic_scanner.gui.models.element_bases.blueprint import BaseBlueprint
from pic_scanner.gui.models.element_bases import GUIFileCollection


class BluePrint(BaseBlueprint):

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

        self.__file_collection = file_collection

        self.__file_collection_cursor = GUIFileCollection(file_collection)

        if pre_built_left_column and isinstance(pre_built_left_column, LeftColumn):
            self.__left_column = pre_built_left_column
        else:
            self.__left_column = LeftColumn(self.file_collection, **kwargs)

        if pre_built_file_column and isinstance(pre_built_file_column, FileColumn):
            self.__file_column = pre_built_file_column
        else:
            self.__file_column = FileColumn(self.file_collection[0], **kwargs)

        super().__init__(**kwargs)

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
        self.file_column.change_image(new_image)

    def current_image(self):
        return self.file_column.file_path

    def next_image(self):
        image = self.file_collection_cursor.next()

    def update_image(self):
        if self.current_image != self.file_collection_cursor.current:
            self.change_image(self.file_collection_cursor.current)
