from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
from typing import Union, Tuple, Optional
import io
from io import BytesIO
import base64
from pic_scanner.helpers import MOD_LOGGER as PARENT_LOGGER
from pathlib import Path
import hashlib

MOD_LOGGER = PARENT_LOGGER.get_child('images')





def draw_bounding_boxes(
        image_path,
        concerns,
        box_color=(255, 0, 0),
        text_color=(255, 255, 255),
        save_path=None,
        save_annotated=False
):
    """
    Draw bounding boxes around areas of concern in an image.

    Parameters:
        image_path (str):
            The path to the image.

        concerns (list):
            The areas of concern in the image.

        save_path (str):
            The path to save the annotated image.

        save_annotated (bool):
            A flag indicating whether to save the annotated image.

    Returns:
        Image:
            The image with the bounding boxes drawn.
    """
    # Load the image
    image = Image.open(image_path)

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Load a font
    font = ImageFont.load_default()

    # Draw bounding boxes around areas of concern
    for concern in concerns:
        # Extract box coordinates
        box = concern.location
        left, top, right, bottom = box

        draw.rectangle([left, top, right, bottom], outline=box_color)

    if save_annotated:
        # Save the image
        if not save_path:
            output_path = os.path.splitext(image_path)[0] + "_annotated.jpg"
        else:
            output_path = save_path
        image.save(output_path)

    image.show()


def get_image_data(file_or_bytes: Union[str, bytes], maxsize: Tuple[int, int] = (1200, 850)) -> bytes:
    """
    Get image data from a file or a bytes object.

    This function opens an image file or a bytes object, resizes it to fit within the given maximum size,
    and returns the image data in PNG format as bytes.

    Parameters:
        file_or_bytes (Union[str, bytes]):
            The path to the image file or a bytes object containing the image data.

        maxsize (Tuple[int, int], optional):
            The maximum size of the image as a (width, height) tuple. Default is (1200, 850).

    Returns:
        bytes: The image data as a byte-string object in PNG format.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        OSError: If the file cannot be opened and identified as an image file.
        ValueError: If the input bytes object cannot be decoded into an image.
    """
    log = MOD_LOGGER.get_child('get_image_data')

    log.debug(f'Received file or bytes: {file_or_bytes}')

    if isinstance(file_or_bytes, str):
        try:
            img = Image.open(file_or_bytes)
        except FileNotFoundError as e:
            log.error(f'File not found: {file_or_bytes}')
            raise e
        except OSError as e:
            log.error(f'Cannot open file: {file_or_bytes}')
            raise e
    else:
        try:
            img = Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception:
            try:
                dataBytesIO = io.BytesIO(file_or_bytes)
                img = Image.open(dataBytesIO)
            except Exception as e:
                log.error(f'Cannot decode bytes: {e}')
                raise ValueError(f'Cannot decode bytes: {e}') from e

    img.thumbnail(maxsize)

    with BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()


def get_image_checksum(image_path: Union[str, Path]):
    """
    Get the checksum of an image file.

    Parameters:
        image_path (Union[str, Path]):
            The path to the image file.

    Returns:
        str: The checksum of the image file.
    """
    if MOD_LOGGER.find_child_by_name('get_image_checksum'):
        log = MOD_LOGGER.find_child_by_name('get_image_checksum')[0]
    else:
        log = MOD_LOGGER.get_child('get_image_checksum')

    log.debug(f'Received image path: {image_path}')

    if isinstance(image_path, str):
        image_path = Path(image_path)

    if not image_path.exists():
        log.error(f'File not found: {image_path}')
        raise FileNotFoundError(f'File not found: {image_path}')

    with open(image_path, 'rb') as f:
        checksum = hashlib.md5(f.read()).hexdigest()

    log.debug(f'Checksum: {checksum}')

    return checksum
