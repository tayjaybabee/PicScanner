import PySimpleGUI as psg

from pic_scanner.helpers.properties import FrozenProperty, freeze_property
from pic_scanner.gui.models.element_bases.metas import AutoBuildMeta, abstractmethod


@freeze_property
class Column(metaclass=AutoBuildMeta):
    """
    A class for building a PySimpleGUI Column.

    This class is used to build a PySimpleGUI Column. It is a subclass of the `AutoBuildMeta` metaclass.

    Properties:
        auto_build (bool):
            A boolean value that determines whether the class should automatically build itself when
            instantiated. This is set to `False` by default. This property is read-only.

        building (bool):
            A boolean value that determines whether the class is currently building itself. This is set to `False` by
            default.

        column (psg.Column):
            The PySimpleGUI Column object. This is built from the layout, and will only have a value if the class is built.

        column_key (str):
            The key for the column. This is used to identify the column in the layout. It is set to `None` by default, and
            after instantiation it is frozen and cannot be changed.

        is_built (bool):
            A boolean value that determines whether the class has been built.

        layout (list):
            A list of elements that make up the layout of the class. This is used to build the column, and is set to
            an empty list by default.
    """
    column_key = FrozenProperty('column_key', allowed_types=str)

    def __init__(self, column_key: str, auto_build=False):
        """
        Initializes the class.

        This method initializes the class by setting the `building` and `is_built` attributes to `False` and the `layout`
        attribute to an empty list. It also sets the `auto_build` attribute to the value of the `auto_build` argument if
        it is a boolean value, otherwise it sets it to `False`.

        Parameters:

            column_key (str):
                The key for the column. This is used to identify the column in the layout. It is set to `None` by default,
                and after instantiation it is frozen and cannot be changed.

            auto_build (bool):
                A boolean value that determines whether the class should automatically build itself when instantiated.
                Defaults to `False`. This property is read-only.
        """
        self._building = False
        self.__column = None
        self.column_key = column_key
        self.__auto_build = auto_build
        self.__built = False
        self.__layout = []

    @property
    def auto_build(self) -> bool:
        """
        Returns the value of the `auto_build` attribute.

        The `auto_build` attribute is a boolean value that determines whether the class should automatically build itself
        when instantiated.

        Returns:
            bool:
        """
        return self.__auto_build

    @auto_build.setter
    def auto_build(self, value):
        """
        Sets the value of the `auto_build` attribute.

        This method is not implemented and will raise a `NotImplementedError` if called.

        Parameters::
            value (Any):
                The value to set the `auto_build` attribute to.

        Returns:

        """
        raise NotImplementedError('The `auto_build` attribute is read-only.')

    @abstractmethod
    def build(self):
        pass

    @property
    def building(self):
        """
        Returns the value of the `building` attribute.

        The `building` attribute is a boolean value that determines whether the class is currently building itself.

        Returns:
            bool:
                The value of the `building` attribute.

        """
        return self._building

    @property
    def _built(self):
        """
        Returns the value of the `built` attribute.

        The `built` attribute is a boolean value that determines whether the class has been built.

        Returns:
            bool (bool):
                The value of the `built` attribute.

        """
        return self.__built

    @_built.setter
    def _built(self, new):
        """
        Sets the value of the `built` attribute.

        Parameters::
            new (bool):
                The value to set the `built` attribute to.

        Returns:
            None
        """
        self.__built = new

    @property
    def column(self):
        """
        Returns the column.

        The column is built from the layout, and will only have a value if the class is built; otherwise it will be `None`.

        Returns:
            psg.Column:
                The column.
        """
        if self.layout and self.building and not self.is_built and self.__column is None:
            self.__column = psg.Column(self.layout, key=self.column_key)
        return self.__column

    @property
    def _column(self):
        """
        Returns the column.

        Returns:
            psg.Column:
                The column.

        """
        return self.__column

    @_column.setter
    def _column(self, new):
        """
        Sets the column.

        Parameters:
            new (psg.Column):
                The new column.

        Returns:
            None
        """
        self.__column = new

    @property
    def layout(self):
        """
        Returns the layout.

        The layout is a list of elements that make up the layout of the class. This is used to build the column, and is
        set to an empty list by default.

        Returns:
            list:
                The layout.
        """
        return self.__layout

    @property
    def _layout(self):
        """
        Returns the layout.

        Returns:
            list:
                The layout.

        """
        return self.__layout

    @_layout.setter
    def _layout(self, new):
        """
        Sets the layout.

        Args:
            new (list):
                The new layout.

        Returns:
            None

        """
        self.__layout = new

    @property
    def is_built(self):
        """
        Returns whether the class has been built.

        Returns:
            bool:
                True if the class has been built, False otherwise.

        """
        return bool(self.layout)
