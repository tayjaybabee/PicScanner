from inspyre_toolbox.syntactic_sweets.properties.decorators import validate_type
from .. import MOD_LOGGER as PARENT_LOGGER
from pic_scanner.log_engine import Loggable


MOD_LOGGER = PARENT_LOGGER.get_child('element_key')


class GUIElementKey(str, Loggable):
    """
    A class to represent the key for a GUI element.

    The class is a subclass of the `str

    Properties:
        prefix_enabled (bool):
            Whether the prefix is enabled.

        prefix (str):
            The prefix for the key.

        suffix_enabled (bool):
            Whether the suffix is enabled.

        suffix (str):
            The suffix for the key.

        pre_formatted (str):
            The pre-formatted key.

        replacement_char (str):
            The character to replace spaces with.

        replace_spaces (bool):
            Whether to replace spaces in the key.

        formatted_key (str):
            The formatted key.

            This property is read-only and consists of the prefix, key, and suffix.

        part_delimiter (str):
            The delimiter for the key parts.
    """

    def __new__(
            cls,
            key: str,
            enable_prefix: bool = False,
            enable_suffix: bool = False,
            prefix: str = None,
            suffix: str = None,
            replace_spaces: bool = False,
            replacement_char: str = '_',
            part_delimiter: str = '_',
            all_upper: bool = True,
            *args,
            **kwargs
            ):
        return super().__new__(cls, key)

    def __init__(
            self,
            key: str,
            enable_prefix: bool = False,
            enable_suffix: bool = False,
            prefix: str = None,
            suffix: str = None,
            replace_spaces: bool = False,
            replacement_char: str = '_',
            part_delimiter: str = '_',
            all_upper: bool = True,
            *args,
            **kwargs
            ):

        str.__init__(self)
        Loggable.__init__(self, parent_log_device=MOD_LOGGER)

        if enable_prefix and not prefix:
            raise ValueError("Prefix is enabled but no prefix was provided.")

        if enable_suffix and not suffix:
            raise ValueError("Suffix is enabled but no suffix was provided.")

        self.__prefix_enabled = False
        self.__prefix = None
        self.__suffix_enabled = False
        self.__suffix = None
        self.__pre_formatted = None
        self.__replacement_char = None
        self.__replace_spaces = False
        self.__formatted = False
        self.__formatted_key = None
        self.__part_delimiter = None
        self.__all_upper = True

        self.__all_upper = all_upper
        self.replacement_char = replacement_char
        self.part_delimiter = part_delimiter
        self.pre_formatted = key
        self.prefix_enabled = enable_prefix
        self.suffix_enabled = enable_suffix
        if prefix:
            self.prefix = prefix

        if suffix:
            self.suffix = suffix
        self.replace_spaces = replace_spaces

    def __str__(self):
        return self.formatted

    def __repr__(self):
        return f"<GUIElementKey object: {self.formatted}>"

    @property
    def all_upper(self):
        """
        Whether the key should be all upper case.

        Returns:
            bool:
                True if the key should be all upper case, False otherwise.
        """
        return self.__all_upper

    @all_upper.setter
    @validate_type(bool)
    def all_upper(self, new: bool):
        """
        Sets the `all_upper` attribute of the key.

        Parameters:
            new (bool):
                The new value for the `all_upper` attribute.

        Returns:
            None
        """
        self.__all_upper = new

    @property
    def part_delimiter_1(self):
        """
        The first part delimiter for the key.

        Returns:
            str:
                The first part delimiter for the key.
        """
        return self.part_delimiter if self.prefix_enabled else ''

    @property
    def part_delimiter_2(self):
        """
        The second part delimiter for the key.

        Returns:
            str:
                The second part delimiter for the key.
        """
        return self.part_delimiter if self.suffix_enabled else ''

    @property
    def prefix_enabled(self) -> bool:
        """
        Whether the prefix is enabled.

        Returns:
            bool:
                True if the prefix is enabled, False otherwise.
        """
        return self.__prefix_enabled if self.prefix else False

    @prefix_enabled.setter
    @validate_type(bool)
    def prefix_enabled(self, new: bool):
        """
        Sets the `prefix_enabled` attribute of the key.

        Parameters:
            new (bool):
                The new value for the `prefix_enabled` attribute.

        Returns:
            None
        """
        self.__prefix_enabled = new

    @property
    def prefix(self) -> str:
        """
        The prefix for the key.

        Returns:
            str:
                The prefix for the key.
        """
        prefix = self.__prefix or ''

        if prefix and self.all_upper:
            prefix = prefix.upper()

        if self.replace_spaces:
            prefix = prefix.replace(' ', self.replacement_char)

        return prefix

    @prefix.setter
    @validate_type(str, None)
    def prefix(self, new: str):
        """
        Sets the `prefix` attribute of the key.

        Parameters:
            new (str):
                The new prefix for the key.

        Returns:
            None
        """
        self.__prefix = new

    @property
    def suffix_enabled(self) -> bool:
        """
        Whether the suffix is enabled.

        Returns:
            bool:
                True if the suffix is enabled, False otherwise.
        """
        return self.__suffix_enabled if self.suffix else False

    @suffix_enabled.setter
    @validate_type(bool)
    def suffix_enabled(self, new: bool):
        """
        Sets the `suffix_enabled` attribute of the key.

        Parameters:
            new (bool):
                The new value for the `suffix_enabled` attribute.

        Returns:
            None
        """
        self.__suffix_enabled = new

    @property
    def suffix(self) -> str:
        """
        The suffix for the key.

        Returns:
            str:
                The suffix for the key.
        """
        suffix = self.__suffix or ''

        if suffix and self.all_upper:
            suffix = suffix.upper()

        if self.replace_spaces:
            suffix = suffix.replace(' ', self.replacement_char)

        return suffix

    @suffix.setter
    @validate_type(str)
    def suffix(self, new: str):
        """
        Sets the `suffix` attribute of the key.

        Parameters:
            new (str):
                The new suffix for the key.

        Returns:
            None
        """
        self.__suffix = new

    @property
    def pre_formatted(self) -> str:
        """
        The pre-formatted key.

        Returns:
            str:
                The pre-formatted key.
        """
        return self.__pre_formatted

    @pre_formatted.setter
    @validate_type(str)
    def pre_formatted(self, new: str):
        """
        Sets the `pre_formatted` attribute of the key.

        Parameters:
            new (str):
                The new pre-formatted key.

        Returns:
            None
        """
        if not self.__pre_formatted:
            self.__pre_formatted = new
        else:
            raise AttributeError("Cannot change pre_formatted attribute after it has been set.")

    @property
    def replacement_char(self) -> str:
        """
        The character to replace spaces with.

        Returns:
            str:
                The character to replace spaces with.
        """
        return self.__replacement_char if self.replace_spaces else ''

    @replacement_char.setter
    @validate_type(str)
    def replacement_char(self, new: str):
        """
        Sets the `replacement_char` attribute of the key.

        Parameters:
            new (str):
                The new replacement character for the key.

        Returns:
            None
        """
        self.__replacement_char = new

    @property
    def replace_spaces(self) -> bool:
        """
        Whether to replace spaces in the key.

        Returns:
            bool:
                True if spaces should be replaced, False otherwise.
        """
        return self.__replace_spaces

    @replace_spaces.setter
    @validate_type(bool)
    def replace_spaces(self, new: bool):
        """
        Sets the `replace_spaces` attribute of the key.

        Parameters:
            new (bool):
                The new value for the `replace_spaces` attribute.

        Returns:
            None
        """
        self.__replace_spaces = new

    @property
    def formatted_key(self) -> str:
        """
        The formatted key.

        Returns:
            str:
                The formatted key.
        """
        key = self.pre_formatted.strip()
        if self.replace_spaces:
            key = key.replace(' ', self.replacement_char)

        if self.all_upper:
            key = key.upper()

        return key

    @property
    def formatted(self):
        """
        The formatted key with the prefix and suffix.

        Returns:
            str:
                The formatted key.
        """
        return f"{self.prefix}{self.part_delimiter_1}{self.formatted_key}{self.part_delimiter_2}{self.suffix}"
