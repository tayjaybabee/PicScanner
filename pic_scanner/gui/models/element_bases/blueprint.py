from pic_scanner.gui.models.element_bases.metas import AutoBuildMeta, abstractmethod


class BaseBlueprint(metaclass=AutoBuildMeta):
    """
    A base class for building blueprints.

    This class is used to create blueprints for building GUI elements. A blueprint is a set of
    instructions that are used to build a GUI element.

    Properties:

        auto_build (bool):
            A boolean value that determines whether the class should automatically build itself when
            instantiated.

        building (bool):
            A boolean value that determines whether the class is currently building itself.

        is_built (bool):
            A boolean value that determines whether the class has been built.

        layout (list):
            A list of elements that make up the layout of the class.

    Methods:

            build():
                An abstract method that builds the class.
    """

    def __init__(self, auto_build: bool = False):
        """
        Initializes the class.

        This method initializes the class by setting the `building` and `is_built` attributes to
        `False` and the `layout` attribute to an empty list. It also sets the `auto_build` attribute
        to the value of the `auto_build` argument if it is a boolean value, otherwise it sets it to
        `False`.

        Parameters:
            auto_build (bool):
                A boolean value that determines whether the class should automatically build itself
                when instantiated. Defaults to `False`.
        """
        self._building = False
        self.__built = False
        self._layout = []
        self.__auto_build = auto_build if isinstance(auto_build, bool) else False

    @property
    def auto_build(self):
        """
        Returns the value of the `auto_build` attribute.

        The `auto_build` attribute is a boolean value that determines whether the class should
        automatically build itself when instantiated.

        Returns:
            bool:
                The value of the `auto_build` attribute.

        """
        return self.__auto_build

    @auto_build.setter
    def auto_build(self, value):
        """
        Sets the value of the `auto_build` attribute.

        This method is not implemented and will raise a `NotImplementedError` if called.

        Parameters:
            value:
                The value to set the `auto_build` attribute to.

        Returns:
            None

        Raises:
            NotImplementedError:
                If the method is called.
        """
        raise NotImplementedError('The `auto_build` attribute is read-only.')

    @property
    def building(self):
        """
        Returns the value of the `building` attribute.

        The `building` attribute is a boolean value that determines whether the class is currently building
        itself.

        Returns:
            bool:
                The value of the `building` attribute.
        """
        return self._building

    @building.deleter
    def building(self):
        """
        Deletes the `building` attribute.

        This method sets the `building` attribute to `False`.

        Returns:
            None
        """
        self._building = False

    @property
    def _built(self):
        """
        Returns the value of the `_built` attribute.

        The `_built` attribute is a boolean value that determines whether the class has been built.

        Returns:
            bool:
                The value of the `_built` attribute.
        """
        return self.__built

    @_built.setter
    def _built(self, new: bool):
        """
        Sets the value of the `_built` attribute.

        This method sets the `_built` attribute to the value of the `new` argument.

        Parameters:
            new (bool):
                The value to set the `_built` attribute to.

        Returns:
            None
        """
        self.__built = new

    @property
    def is_built(self):
        """
        Returns the value of the `is_built` attribute.

        The `is_built` attribute is a boolean value that determines whether the class has been built.

        Returns:
            bool:
                The value of the `is_built` attribute.
        """
        return self._built

    @property
    def layout(self):
        """
        Returns the value of the `layout` attribute.

        The `layout` attribute is a list of elements that make up the layout of the class.

        Returns:
            list:
                The value of the `layout` attribute.
        """
        return self._layout

    @abstractmethod
    def build(self):
        """
        An abstract method that builds the class.

        This method is called to build the class by creating and must be implemented by subclasses.

        Returns:
            None
        """
        pass
