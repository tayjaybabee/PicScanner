from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
from typing import Union, Tuple, Optional
from io import BytesIO
import base64





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


def get_image_data(file, maxsize=(1200, 850), first=False):
    """
    Get image data from a file.

    Parameters:
        file (str):
            The path to the file.

        maxsize (tuple):
            The maximum size of the image.

        first (bool):
            A flag indicating whether to return the first image.
    """
    img = Image.open(file)
    img.thumbnail(maxsize)

    if first:
        bio = BytesIO()
        img.save(bio, format='PNG')
        del img

        return bio.getvalue()

    return ImageTk.PhotoImage(img)
