from . import GUIElementKey, MOD_LOGGER as PARENT_LOGGER, Loggable


MOD_LOGGER = PARENT_LOGGER.get_child('factories')


class GUIElementKeyFactory(Loggable):
    """
    A factory class to create GUIElementKey objects with predefined configurations.
    """

    def __init__(
            self,
            default_prefix=None,
            default_suffix=None,
            default_replacement_char='_',
            default_part_delimiter='_',
            default_all_upper=True,
            default_replace_spaces=True,
            skip_sample=True,
            ):
        super().__init__(parent_log_device=MOD_LOGGER)
        log = self.log_device
        self.default_prefix = default_prefix
        log.debug(f'Set the default prefix to: {default_prefix}')

        self.default_suffix = default_suffix
        log.debug(f'Set the default suffix to: {default_suffix}')

        self.default_replacement_char = default_replacement_char
        log.debug(f'Set the default replacement character to: {default_replacement_char}')

        self.default_part_delimiter = default_part_delimiter
        log.debug(f'Set the default part delimiter to: {default_part_delimiter}')

        self.default_all_upper = default_all_upper
        log.debug(f'Set the default all upper case to: {default_all_upper}')

        self.default_replace_spaces = default_replace_spaces
        log.debug(f'Set the default replace spaces to: {default_replace_spaces}')

        if not skip_sample:
            self.sample_key = self.create_key('sample')

    def create_key(
            self,
            key: str,
            enable_prefix: bool = False,
            enable_suffix: bool = False,
            prefix: str = None,
            suffix: str = None,
            replace_spaces: bool = None,
            replacement_char: str = None,
            part_delimiter: str = None,
            all_upper: bool = None
            ) -> GUIElementKey:
        """
        Create a GUIElementKey with the specified parameters, falling back to factory defaults where necessary.

        Parameters:
            key (str):
                The base key string.

            enable_prefix (bool):
                Whether to enable the prefix.

            enable_suffix (bool):
                Whether to enable the suffix.

            prefix (str):
                The prefix to use. Defaults to the factory default.

            suffix (str):
                The suffix to use. Defaults to the factory default.

            replace_spaces (bool):
                Whether to replace spaces in the key.

            replacement_char (str):
                The character to replace spaces with. Defaults to the factory default.

            part_delimiter (str):
                The delimiter for the key parts. Defaults to the factory default.

            all_upper (bool):
                Whether to convert the key to all upper case. Defaults to the factory default.

        Returns:
            GUIElementKey:
            `   The configured GUI element key.
        """
        log_name = f'{self.log_device.name}:create_key'

        log = (
            self.log_device.find_child_by_name(log_name)[0]
            ) if self.log_device.has_child(log_name) else self.create_child_logger()

        prefix = prefix if prefix is not None else self.default_prefix
        log.debug(f'Set the prefix to: {prefix}')

        if prefix:
            enable_prefix = True
            log.debug(f'Enabled the prefix: {enable_prefix} due to the presence of a prefix')
        else:
            log.debug(f'Disabled the prefix: {enable_prefix} due to the absence of a prefix')

        suffix = suffix if suffix is not None else self.default_suffix
        log.debug(f'Set the suffix to: {suffix}')

        if suffix:
            enable_suffix = True
            log.debug(f'Enabled the suffix: {enable_suffix} due to the presence of a suffix')
        else:
            log.debug(f'Disabled the suffix: {enable_suffix} due to the absence of a suffix')

        replacement_char = replacement_char if replacement_char is not None else self.default_replacement_char
        log.debug(f'Set the replacement character to: {replacement_char}')

        part_delimiter = part_delimiter if part_delimiter is not None else self.default_part_delimiter
        log.debug(f'Set the part delimiter to: {part_delimiter}')

        all_upper = all_upper if all_upper is not None else self.default_all_upper
        log.debug(f'Set the all upper case to: {all_upper}')

        replace_spaces = replace_spaces if replace_spaces is not None else self.default_replace_spaces
        log.debug(f'Set the replace spaces to: {replace_spaces}')

        return GUIElementKey(
            key=key,
            enable_prefix=enable_prefix,
            enable_suffix=enable_suffix,
            prefix=prefix,
            suffix=suffix,
            replace_spaces=True,
            replacement_char=replacement_char,
            part_delimiter=part_delimiter,
            all_upper=all_upper
        )
