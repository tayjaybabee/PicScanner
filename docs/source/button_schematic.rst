ButtonSchematic
===============

This module provides base functionality for creating buttons in the GUI.

.. module:: button_schematic
    :platform: Any
    :synopsis: Base functionality for creating buttons in the GUI.
.. moduleauthor:: Your Name <your.email@example.com>

Overview
--------

The `ButtonSchematic` class provides a structured way to create and manage buttons in a PySimpleGUI application. It ensures unique keys for buttons and allows for various configurations such as auto-building, visibility, and enable/disable states.

Usage
-----

Import the necessary modules and create an instance of `ButtonSchematic`:

.. code-block:: python

    from pic_scanner.gui.models.element_bases.button_schematic import ButtonSchematic

    # Create a ButtonSchematic instance
    button = ButtonSchematic(
        text='My Button',
        auto_build=True,
        key='MY_BUTTON',
        create_disabled=False,
        create_hidden=False,
        skip_enforcing_unique_keys=False
    )

Attributes
----------

The `ButtonSchematic` class has several attributes that can be used to customize the behavior and appearance of the button:

- **text**: The text to display on the button.
- **auto_build**: Whether the button should be built automatically.
- **create_disabled**: Whether the button should be created in a disabled state.
- **create_hidden**: Whether the button should be created in a hidden state.
- **key**: The key for the button.
- **enforce_unique_keys**: Whether to enforce unique keys for buttons.
- **built**: Whether the button has been built.
- **button**: The PySimpleGUI button object.
- **state**: A `Box` object containing the state of the button, including whether it is enabled and visible.

Methods
-------

The `ButtonSchematic` class provides several methods for managing buttons:

- **has_key(key, case_sensitive=False, return_instance=False)**: Checks if the class instances dictionary contains the provided key.
- **get_instance(key, default=None, case_sensitive=False)**: Returns an instance from the class instances dictionary based on the provided key.
- **check_key(key, case_sensitive=False)**: Check if the key is in the `ButtonSchematic.instances` dictionary.
- **build()**: Build the button.
- **disable()**: Disables the button.
- **enable()**: Enables the button.
- **hide()**: Hides the button.
- **unhide()**: Unhides the button.
- **update(**kwargs)**: Updates the button.

Examples
--------

Creating and building a button:

.. code-block:: python

    button = ButtonSchematic(
        text='Submit',
        auto_build=True
    )

    button.build()

    if button.built:
        print("Button has been built successfully.")

Disabling and enabling a button:

.. code-block:: python

    button.disable()
    if button.disabled:
        print("Button is disabled.")

    button.enable()
    if button.enabled:
        print("Button is enabled.")

Hiding and unhiding a button:

.. code-block:: python

    button.hide()
    if button.hidden:
        print("Button is hidden.")

    button.unhide()
    if button.visible:
        print("Button is visible.")

Updating the button's properties:

.. code-block:: python

    button.update(text='Click Me', visible=True)

Check if a key exists and get an instance:

.. code-block:: python

    if ButtonSchematic.has_key('MY_BUTTON'):
        instance = ButtonSchematic.get_instance('MY_BUTTON')
        print(f"Button instance: {instance}")

Note: Ensure the key used for the button is unique if `enforce_unique_keys` is set to True. Otherwise, a `ValueError` will be raised.

Conclusion
----------

The `ButtonSchematic` class is a versatile tool for creating and managing buttons in a PySimpleGUI application. It ensures consistency and provides a variety of configurations to suit different needs. By using the provided methods and attributes, developers can efficiently manage the state and behavior of buttons in their applications.
