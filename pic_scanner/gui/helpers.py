

def format_button_key(
        text: str,
        skip_space_replacement=False,
        replace_spaces_with='_',
        skip_uppercase_conversion=False,
        skip_suffix=False,
        suffix='button',
    ) -> str:
    """
    Format a button key based on the provided text.

    The function will optionally perform the following actions:
        - Replace spaces in the string with a specified character (default is '_')
        - Convert the text to uppercase
        - Append a suffix to the text (default is 'button')

    Parameters:
        text (str):
            The text to format.

        skip_space_replacement (bool):
            Whether to skip replacing spaces in the text. Default is False.

        replace_spaces_with (str):
            The character to replace spaces with. Default is '_'.

        skip_uppercase_conversion (bool):
            Whether to skip converting the text to uppercase. Default is False.

        skip_suffix (bool):
            Whether to skip appending a suffix to the text. Default is False.

        suffix (str):
            The suffix to append to the text. Default is 'button'.

    Returns:
        str:
            The formatted button key.

    Examples:
        >>> format_button_key('My Button')
        'MY_BUTTON_BUTTON'

        >>> format_button_key('My Button', skip_suffix=True)
        'MY_BUTTON'

        >>> format_button_key('My Button', skip_uppercase_conversion=True)
        'My_button'

        >>> format_button_key('My Button', skip_space_replacement=True)
        'MY BUTTON button'

        >>> format_button_key('My Button', replace_spaces_with='-')
        'MY-BUTTON_button'
    """
    formatted_text = text
    print(f"formatted_text: {formatted_text}")

    if not skip_suffix:
        formatted_text = f"{formatted_text} {suffix}"

    print(f"formatted_text: {formatted_text}")

    if not skip_uppercase_conversion:
        formatted_text = formatted_text.upper()

    print(f"formatted_text: {formatted_text}")

    if not skip_space_replacement:
        formatted_text = formatted_text.replace(' ', replace_spaces_with)

    print(f"formatted_text: {formatted_text}")

    return formatted_text
