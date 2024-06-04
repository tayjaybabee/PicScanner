import os


def is_windows() -> bool:
    """
    Check if the current operating system is Windows.

    Returns:
        bool:
            True if the current operating system is Windows, False otherwise.
    """
    return os.name == 'nt'
