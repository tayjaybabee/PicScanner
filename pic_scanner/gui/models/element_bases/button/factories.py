from pic_scanner.gui.models.element_bases.button import ButtonSchematic, MOD_LOGGER as PARENT_LOGGER, Loggable
from pic_scanner.gui.models.element_bases.element_key.factories import GUIElementKeyFactory


MOD_LOGGER = PARENT_LOGGER.get_child('factories')


class ButtonFactory(Loggable):
    """
    A class to create ButtonSchematic instances.

    Properties:
        instances (dict):
            A dictionary of instances of the ButtonFactory.

    Methods:
        __new__:
            Create a new instance of the ButtonFactory if one does not already exist.

        __init__:
            Initialize the ButtonFactory.

        create_button -> ButtonSchematic:
            Create a ButtonSchematic with the specified parameters, falling back to factory defaults
            where necessary.
    """
    instances = {}

    def __new__(cls, window_name: str, *args, **kwargs):
        if window_name in cls.instances:
            return cls.instances[window_name]
        else:
            return super().__new__(cls)

    def __init__(
            self,
            window_name: str,
            default_auto_build=False,
            default_size=None,
            default_hidden=False,
            default_disabled=False,
            key_factory=None
            ):
        """
        Initialize the ButtonFactory.

        Parameters:
            window_name (str):
                The name of the window.

            default_auto_build (bool):
                The default auto build value.

            default_size (tuple):
                The default size of the button.

            default_hidden (bool):
                The default hidden value.

            default_disabled (bool):
                The default disabled value.

            key_factory (GUIElementKeyFactory):
                The key factory.
        """
        super().__init__(parent_log_device=MOD_LOGGER)
        self.window_name = window_name
        self.default_auto_build = default_auto_build
        self.default_size = default_size
        self.default_hidden = default_hidden
        self.default_disabled = default_disabled
        self.key_factory = key_factory or GUIElementKeyFactory(
                default_prefix=window_name,
                default_suffix='button',
                default_replace_spaces=True,
                default_replacement_char='_',
                default_part_delimiter=':',
                default_all_upper=True,
                skip_sample=True

                    )
        self.instances[window_name] = self

    def create_button(
            self,
            text: str,
            auto_build: bool = None,
            size: tuple = None,
            hidden: bool = None,
            disabled: bool = None,
            key: str = None,
        ):
        """
        Create a ButtonSchematic with the specified parameters, falling back to factory defaults
        where necessary.

        Parameters:
            text (str):
                The text for the button.

            auto_build (bool):
                Whether the button should be built automatically.

            size (tuple):
                The size of the button.

            hidden (bool):
                Whether the button should be hidden.

            disabled (bool):
                Whether the button should be disabled.

            key (str):
                The key for the button.

        Returns:
            ButtonSchematic:
                The ButtonSchematic instance.
        """
        auto_build = auto_build or self.default_auto_build

        if size is None:
            size = self.default_size
        else:
            size = size if isinstance(size, tuple) else self.default_size

        if hidden is None:
            hidden = self.default_hidden
        else:
            hidden = hidden if isinstance(hidden, bool) else self.default_hidden

        if disabled is None:
            disabled = self.default_disabled

        else:
            disabled = disabled if isinstance(disabled, bool) else self.default_disabled

        if key is None:
            if self.key_factory:
                key = self.key_factory.create_key(text)
            else:
                key = text
        else:
            if self.key_factory:
                key = self.key_factory.create_key(key)
            else:
                if isinstance(key, str):
                    key = key
                else:
                    raise ValueError('The key must be a string.')

        return ButtonSchematic(
                text=text,
                auto_build=auto_build,
                size=size,
                hidden=hidden,
                disabled=disabled,
                key=key
                )
