from pathlib import Path
from typing import Union, Optional
import requests

from ..common.constants import DEFAULT_BASE_URL
from ..helpers.filesystem import provision_path



def create_payload(
        image_path:  Union[str, Path],
        do_not_expand: bool = False,
        do_not_resolve: bool = False,
        do_not_convert: bool = False,
        do_not_provision: bool = False
):
    """
    Create a payload for the request.

    Parameters:
        image_path (str):
            The path to the image.

        do_not_expand (bool):
            A flag indicating whether to expand the path.

        do_not_resolve (bool):
            A flag indicating whether to resolve the path.

        do_not_convert (bool):
            A flag indicating whether to convert the path to a string.

    Returns:
        dict:
            The payload for the request.

    Raises:
        ValueError:
            If the path is invalid.
    """
    if not do_not_provision:
        image_path = provision_path(
            image_path,
            do_not_expand=do_not_expand,
            do_not_resolve=do_not_resolve,
            do_not_convert=do_not_convert
        )

    if not isinstance(image_path, Path):
        raise ValueError(f"Invalid path: {image_path}!")

    if not image_path.exists():
        raise FileNotFoundError(f"The file {image_path} does not exist!")

    return {'f1': open(image_path, 'rb')}


def make_request(
        image_path:       Union[str, Path],
        base_url:         Optional[str] = DEFAULT_BASE_URL,
        do_not_expand:    bool = False,
        do_not_resolve:   bool = False,
        do_not_convert:   bool = False,
        do_not_provision: bool = False
):
    """
    Make a request to the inference server.

    Parameters:
        image_path (Union[str, Path]):
            The path to the image.

        base_url (str):
            The base URL of the inference server.

        do_not_expand (bool):
            A flag indicating whether to expand the path.

        do_not_resolve (bool):
            A flag indicating whether to resolve the path.

        do_not_convert (bool):
            A flag indicating whether to convert a string to a pathlib.Path object.

        do_not_provision (bool):
            A flag indicating whether to provision the path.

    Returns:
        dict:
            The result of the request.

    Raises:
        requests.exceptions.HTTPError:
            If the request was unsuccessful.

        ValueError:
            If the path is invalid.

        FileNotFoundError:
            If the file does not exist.

        PermissionError:
            If the file is not accessible.

        IsADirectoryError:
            If the path is a directory.
    """
    # Create the payload
    files = create_payload(
        image_path,
        do_not_expand=do_not_expand,
        do_not_resolve=do_not_resolve,
        do_not_convert=do_not_convert,
        do_not_provision=do_not_provision
    )

    # Make the request
    response = requests.post(base_url, files=files)

    # Check if the request was successful
    response.raise_for_status()

    return response.json()


def analyze_image(
        image_path: Union[str, Path],
        base_url: Optional[str] = None,
        do_not_provision: bool = False,
        do_not_convert: bool = False,
        **kwargs
) -> dict:
    """
    Analyze an image using the inference server.

    Parameters:
        image_path (str):
            The path to the image.

        base_url (Optional[str]):
            The base URL of the inference server.

    Returns:
        dict:
            The result of the analysis.
    """
    if base_url is None:
        base_url = DEFAULT_BASE_URL

    if not do_not_provision:
        image_path = provision_path(image_path, do_not_convert=do_not_convert, **kwargs)

    result = make_request(image_path, base_url=base_url, do_not_provision=True)

    return {
        'image_path': image_path,
        'result': result

    }
