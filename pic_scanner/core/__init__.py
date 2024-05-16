from typing import Union, Optional
from pathlib import Path
from pic_scanner.models.image import create_scanned_image, ScannedImageCollection, ScannedImage
from pic_scanner.helpers.filesystem import provision_path
from pic_scanner.api import analyze_image
from tqdm import tqdm
from warnings import warn


__all__ = [
    'scan_image',
    'scan_images'
]


def scan_image(image_path: Union[str, Path], base_url: Optional[str] = None) -> ScannedImage:
    """
    Scan an image for NSFW content.

    Parameters:
        image_path (Union[str, Path]):
            The path to the image to scan.

        base_url (Optional[str]):
            The base URL of the API to use.

    Returns:
        ScannedImage:
            The scanned image.

    Raises:
        ValueError:
            If the image path is invalid.
    """
    res_data = analyze_image(image_path, base_url=base_url)
    scanned_image = create_scanned_image(res_data)

    return scanned_image


def scan_images(
        image_paths: Union[list[Union[str, Path]], Path],
        base_url: Optional[str] = None,
        do_not_convert_paths: bool = False,
        do_not_provision_paths: bool = False,
        prog_bar: bool = False,
        **kwargs
) -> ScannedImageCollection:
    """
    Scan a collection of images for NSFW content.

    Parameters:
        image_paths (Union[list[Union[str, Path]], Path]):
            The paths to the images to scan.

        base_url (Optional[str]):
            The base URL of the API to use.

        do_not_convert_paths (bool):
            A flag indicating whether to convert the paths to strings.

        do_not_provision_paths (bool):
            A flag indicating whether to provision the paths.

        prog_bar (bool):
               A flag indicating whether to display a progress bar.

    Returns:
        ScannedImageCollection:
            The scanned images.

    Raises:
        ValueError:
            If the image paths are invalid.

    """
    scanned_images = ScannedImageCollection()
    failed_images = []

    if not isinstance(image_paths, list):
        if isinstance(image_paths, Path):
            image_paths = [image_paths]

        elif isinstance(image_paths, str) and not do_not_convert_paths:
            image_paths = [Path(image_paths)]

    if prog_bar:
        image_paths = tqdm(image_paths)

    for image_path in image_paths:
        if not isinstance(image_path, Path) and not do_not_convert_paths:
            image_path = Path(image_path)

        if not do_not_provision_paths:
            image_path = provision_path(
                image_path,
                do_not_convert=do_not_convert_paths,
                **kwargs
            )

        try:

            result = analyze_image(image_path, base_url=base_url, do_not_provision=True)

            scanned_image = create_scanned_image(result)
        except Exception as e:
            if e.__class__.__name__ == 'KeyboardInterrupt':
                raise e from e
            failed_images.append(image_path)
            warn(f"Failed to scan image: {image_path} {result if hasattr(locals(), 'result') else ''}!")
            continue

        scanned_images.add_image(scanned_image)

    return scanned_images
