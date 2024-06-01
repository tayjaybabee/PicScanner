"""
This module provides base functionality for creating buttons in the GUI.
"""

from box import Box
from PySimpleGUI import Button
from inspyre_toolbox.syntactic_sweets.properties.decorators import validate_type
from pic_scanner.log_engine import Loggable
from pic_scanner.gui.models.element_bases import MOD_LOGGER as PARENT_LOGGER
from pic_scanner.gui.models.element_bases.element_key.factories import GUIElementKeyFactory, GUIElementKey

from typing import Union


MOD_LOGGER = PARENT_LOGGER.get_child('button')


class ButtonSchematic(Loggable):
    instances = {}
    built_instances = {}

    DEFAULT_SUFFIX = 'button'

    suffix = DEFAULT_SUFFIX

    @classmethod
    def has_key(cls, key: str, case_sensitive=False, return_instance=False) -> Union[bool, 'ButtonSchematic', None]:
        """
        Checks if the class instances dictionary contains the provided key with optional case sensitivity and instance return.

        Parameters:
            key (str):
                The key to check in the `ButtonSchematic.instances` dictionary.

            case_sensitive (bool):
                Whether the key comparison should be case-sensitive. Default is False.

            return_instance (bool):
                Whether to return the instance corresponding to the key. Default is False.

        Returns:
            Union[bool, 'ButtonSchematic', None]:
                - If return_instance is False: True if the key is present in the instances dictionary, False otherwise.
                - If return_instance is True: The instance corresponding to the key, or None if the key is not found.

        Examples:
            >>> ButtonSchematic.has_key('MY_BUTTON')
            False

            >>> ButtonSchematic.has_key('MY_BUTTON', case_sensitive=True)
            True

            >>> ButtonSchematic.has_key('MY_BUTTON', return_instance=True)
            None

            >>> ButtonSchematic.has_key('MY_BUTTON', case_sensitive=True, return_instance=True)
            <ButtonSchematic object at 0x000001>
        """
        if return_instance:
            return cls.get_instance(key, case_sensitive=case_sensitive)
        else:
            return cls.check_key(key, case_sensitive=case_sensitive)

    @classmethod
    def get_instance(cls, key: str, default=None, case_sensitive=False) -> 'ButtonSchematic' or None:
        """
        Returns an instance from the class instances dictionary based on the provided key.

        Parameters:
            key (str):
                The key to look up in the `ButtonSchematic.instances` dictionary.

            default:
                The default value to return if the key is not found. Default is None.

            case_sensitive (bool):
                Whether the key lookup should be case-sensitive. Default is False.

        Returns:
            The instance corresponding to the key, or the default value if the key is not found.

        Examples:
            >>> ButtonSchematic.get_instance('MY_BUTTON')
            None

            >>> ButtonSchematic.get_instance('MY_BUTTON', default='DEFAULT')
            'DEFAULT'

            >>> ButtonSchematic.get_instance('MY_BUTTON', default='DEFAULT', case_sensitive=True)
            None
        """

        if case_sensitive:
            return cls.instances.get(key, default)
        else:
            return cls.instances.get(key.upper(), default)

    @classmethod
    def check_key(cls, key: str, case_sensitive=False) -> bool:
        """
        Check if the key is in the `ButtonSchematic.instances` dictionary.

        Parameters:
            key (str):
                The key to check in the `ButtonSchematics.instances` dictionary.

            case_sensitive (bool):
                Whether the key comparison should be case-sensitive. Default is False.

        Returns:
            bool:
                True if the key is in the instances dictionary, False otherwise.

        Examples:
            >>> ButtonSchematic.check_key('MY_BUTTON')
            False

            >>> ButtonSchematic.check_key('MY_BUTTON', case_sensitive=True)
            True
        """
        return key in cls.instances if case_sensitive else key.upper() in cls.instances


    def __init__(
            self,
            text: str,
            auto_build=False,
            key: str = None,
            create_disabled=False,
            create_hidden=False,
            skip_enforcing_unique_keys=False,
            key_factory: GUIElementKeyFactory = None,
            **kwargs
            ):
        super().__init__(parent_log_device=MOD_LOGGER)

        self._built = False
        self.__enforce_unique_keys = None

        self.__auto_build = False

        self.__create_disabled = False
        self.__create_hidden = False
        self.__key = None
        self.text = text

        self.kwargs = kwargs
        self.__button = None

        self.LOG = self.log_device

        self.LOG.debug(f"Creating ButtonSchematic with text: '{text}' and key: '{key}'")

        self.enforce_unique_keys = not skip_enforcing_unique_keys

        if key_factory and isinstance(key_factory, GUIElementKeyFactory):
            self.key = key_factory.create_key(text)

        self.key = key or text
        self.create_disabled = create_disabled
        self.create_hidden = create_hidden

        ButtonSchematic.instances[self.key] = self

        self.auto_build = auto_build

    def build(self):
        """
        Build the button.

        Building the button will create the button object and store it in the `ButtonSchematic.instances` dictionary.

        Returns:
            None
        """
        # If the button has not already been built and there's nothing in the `self.button` attribute;
        #     - Create the button,
        #     - Assign the button to the `self.button` attribute,
        #     - Set the `built` attribute to True,
        #     - Add the button to the `ButtonSchematic.instances` dictionary.
        if not self.built and not self.__button and self.key in self.instances:
            self.__button = Button(
                    self.text,
                    key=self.key,
                    disabled=self.create_disabled,
                    visible=not self.create_hidden,
                    **self.kwargs
                    )
            self._built = True
            self.instances.pop(self.key)
            self.built_instances[self.key] = self

        # If the button has already been built, whether in this instance or another, log a warning.
        if self.key in self.instances:
            self.LOG.warning(f"Button with key '{self.key}' has already been built.")
            if self.__button is None:
                self.__button = self.instances[self.key].button
                return
            return

        if self.button:
            self.LOG.debug(f"Button with key '{self.key}' has been built.")
        else:
            self.LOG.error(f"Button with key '{self.key}' could not be built.")

    def disable(self):
        """
        Disables the button.

        Returns:
            None
        """
        if self.built:
            self.__button.update(disabled=True)
        else:
            self.__create_disabled = True

    def enable(self):
        """
        Enables the button.

        Returns:
            None
        """
        if self.built:

            self.__button.update(disabled=False)

        else:
            self.__create_disabled = False

    def hide(self):
        """
        Hides the button.

        Returns:
            None
        """
        if self.built:
            self.__button.update(visible=False)
        else:
            self.create_hidden = True

    def unhide(self):
        """
        Unhides the button.

        Returns:
            None

        """
        if self.built and not self.visible:
            self.__button.update(visible=True)
        else:
            self.create_hidden = False

    def update(self, **kwargs):
        """
        Updates the button.

        Returns:
            None
        """

        if self.built:
            self.button.update(**kwargs)
        else:
            self.LOG.error("Cannot update button that has not been built.")


    @property
    def auto_build(self):
        """
        Whether the button should be built automatically.

        Returns:
            bool:
                True if the button should be built automatically, False otherwise.

        Examples:
            >>> button = ButtonSchematic('My Button')
            >>> button.auto_build
            False
        """
        return self.__auto_build

    @auto_build.setter
    @validate_type(bool)
    def auto_build(self, new):
        """
        Sets the `auto_build` attribute of the button.

        A button with `auto_build` set to True will be built automatically.

        Parameters:
            new (bool):
                The new value for the `auto_build` attribute.

        Returns:
            None

        Raises:
            AttributeError:
                If the button has already been built.

        """
        prev = self.__auto_build
        if not self.built:
            self.__auto_build = new
        else:
            raise AttributeError("Cannot change auto_build attribute after the button has been built.")

        if new and not prev:
            self.build()

    @property
    def built(self):
        """
        Whether the button has been built.

        Returns:
            bool:
                True if the button has been built, False otherwise.
        """
        return self._built

    @property
    def button(self) -> Button or None:
        """
        The PySimpleGUI button object.
        """
        return self.__button

    @property
    def create_disabled(self) -> bool:
        """
        Whether the button should be created in a disabled state.

        Returns:
            bool:
                True if the button should be created in a disabled state, False otherwise.
        """
        return self.__create_disabled

    @create_disabled.setter
    @validate_type(bool)
    def create_disabled(self, new):
        """
        Sets the `create_disabled` attribute of the button.

        Parameters:
            new (bool):
                The new value for the `create_disabled` attribute.

        Returns:
            None

        """
        if not self.built:
            self.__create_disabled = new
        else:
            raise AttributeError("Cannot change create_disabled attribute after the button has been built.")

    @property
    def create_hidden(self):
        """
        Whether the button should be created in a hidden state.

        Returns:
            bool:
                True if the button should be created in a hidden state, False otherwise.
        """
        return self.__create_hidden

    @create_hidden.setter
    @validate_type(bool)
    def create_hidden(self, new):
        """
        Sets the `create_hidden` attribute of the button.

        Parameter:
            new (bool):
                The new value for the `create_hidden` attribute.

        Returns:
            None

        """
        if self.built:
            raise AttributeError("Cannot change create_hidden attribute after the button has been built.")

        self.__create_hidden = new

    @property
    def disabled(self):
        """
        Whether the button is disabled.

        Returns:
            bool:
                True if the button is disabled, False otherwise.
        """
        return self.__button.Disabled if self.built else self.__create_disabled

    @property
    def enabled(self):
        """
        Whether the button is enabled.

        Returns:
            bool:
                True if the button is enabled, False otherwise.
        """
        return not self.disabled

    @property
    def enforce_unique_keys(self):
        """
        Whether to enforce unique keys for buttons.

        Returns:
            bool:
                True if unique keys are enforced, False otherwise.
        """
        return self.__enforce_unique_keys

    @enforce_unique_keys.setter
    @validate_type(bool)
    def enforce_unique_keys(self, new):
        """
        Sets the `enforce_unique_keys` attribute of the button.

        Parameters:
            new (bool):
                The new value for the `enforce_unique_keys` attribute.

        Returns:
            None

        """
        if self.built:
            raise AttributeError("Cannot change enforce_unique_keys attribute after the button has been built.")

        self.__enforce_unique_keys = new

    @property
    def hidden(self):
        return not self.visible

    @property
    def key(self):
        """
        The key for the button.

        Returns:
            str:
                The key for the button.
        """
        return self.__key

    @key.setter
    @validate_type(str)
    def key(self, new):
        """
        Sets the `key` attribute of the button.

        Parameters:
            new (str):
                The new key for the button.

        Returns:
            None
        """
        if self.built:
            raise AttributeError("Cannot change key attribute after the button has been built.")

        if isinstance(new, GUIElementKey):
            key = new
        else:
            key = GUIElementKey(
                    new,
                    suffix=self.suffix,
                    enable_suffix=True,
                    replace_spaces=True,
                    prefix='main window',
                    enable_prefix=True,
                    part_delimiter=':',
                    all_upper=True,

                )

        if self.enforce_unique_keys and self.has_key(key):
            raise ValueError(f"Key '{key}' is already in use.")

        self.__key = key

    @property
    def state(self):
        """
        Returns a `Box` object containing the state of the button, including whether it is enabled
        and visible.

        Returns:
            Box:
                A `Box` object with the button's state attributes.

        Examples:
            >>> button = ButtonSchematic('My Button')
            >>> button.state
            {'enabled': False, 'visible': False}
        """

        return Box({
                'enabled': self.enabled,
                'visible': self.visible,
                })

    @property
    def text(self) -> str:
        """
        The text for display on the button.

        Returns:
            str:
                The text for the button.
        """
        return self.__text

    @text.setter
    @validate_type(str)
    def text(self, new: str):
        """
        Sets the `text` attribute of the button.

        Parameters:
            new (str):
                The new text for the button.

        Returns:
            None

        Raises:
            AttributeError:
                If the button has already been built.
        """
        if self.built:
            raise AttributeError("Cannot change text attribute after the button has been built.")

        self.__text = format_button_text(new)

    @property
    def visible(self):
        """
        Whether the button is visible.

        Returns:
            bool:
                True if the button is visible, False otherwise.
        """
        return self.__button.visible if self.built else False



def format_button_text(text: str, skip_titalize=False):
    """
    Format a button text.

    Parameters:
        text (str):
            The text to format.

        skip_titalize (bool):
            Whether to skip titalizing the text. (Default: False)

    Returns:
        str:
            The formatted button text.

    Examples:
        >>> format_button_text('my button')
        'My Button'

        >>> format_button_text('my button', skip_titalize=True)
        'my button'

    """
    if not skip_titalize:
        text = text.title()

    return text
