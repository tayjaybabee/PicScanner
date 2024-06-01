from typing import Union, Optional
from pathlib import Path
from pic_scanner.models.image import create_scanned_image, ScannedImageCollection, ScannedImage
from pic_scanner.helpers.filesystem import provision_path
from pic_scanner.api import analyze_image
from pic_scanner.log_engine import ROOT_LOGGER as PARENT_LOGGER
from tqdm import tqdm
from warnings import warn
from queue import Queue
from threading import Thread


__all__ = [
    'scan_image',
    'scan_images'
]


MOD_LOGGER = PARENT_LOGGER.get_child('core')


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
    if MOD_LOGGER.find_child_by_name('scan_image'):
        log = MOD_LOGGER.find_child_by_name('scan_image')[0]
    else:
        log = MOD_LOGGER.get_child('scan_image')

    res_data = analyze_image(image_path, base_url=base_url)
    log.debug(f'Creating scanned image from result data: {res_data}')

    scanned_image = create_scanned_image(res_data)
    log.debug(f'Scanned image created: {scanned_image}')

    return scanned_image


class Worker(Thread):
    def __init__(self, queue, collection, enable_progress_bar=False, prog_bar=None):
        Thread.__init__(self)
        self.queue = queue
        self.collection = collection
        self.prog_bar = None
        self.enable_progress_bar = enable_progress_bar

        if self.enable_progress_bar:
            self.prog_bar = prog_bar

        print(self.getName())

    def run(self):
        while True:
            image_path = self.queue.get()
            if image_path is None:
                break

            try:
                result = analyze_image(image_path)
                scanned_image = create_scanned_image(result)
                self.collection.add_image(scanned_image)
            except Exception as e:
                warn(f'Failed to scan image: {image_path}', exc_info=True)
            finally:
                self.queue.task_done()
                if self.enable_progress_bar:
                    self.prog_bar.update(1)



def scan_images(
        image_paths: Union[list[Union[str, Path]], Path],
        base_url: Optional[str] = None,
        do_not_convert_paths: bool = False,
        do_not_provision_paths: bool = False,
        prog_bar: bool = False,
        threaded: bool = False,
        num_threads: int = 8,
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

    if MOD_LOGGER.find_child_by_name('scan_images'):
        log = MOD_LOGGER.find_child_by_name('scan_images')[0]
    else:
        log = MOD_LOGGER.get_child('scan_images')

    if not isinstance(image_paths, list):
        log.warning(f'Image paths is not a list: {type(image_paths)}')

        if isinstance(image_paths, Path):
            log.debug(f'Found single Path object: {image_paths}. Converting to list.')
            image_paths = [image_paths]
            log.debug(f'Converted to list: {image_paths}')

        elif isinstance(image_paths, str) and not do_not_convert_paths:
            log.debug(f'Found single string object: {image_paths}. Converting to list of a single '
                      'Path object.')
            image_paths = [Path(image_paths)]
            log.debug(f'Converted to list: {image_paths}')

    log.debug('Checking list of image paths to ensure they are all Path objects and provisioning '
              'them if necessary...')
    for i, image_path in enumerate(image_paths):
        if not isinstance(image_path, Path) and not do_not_convert_paths:
            log.debug(f'Converting image path at index {i} to Path object...')
            image_paths[i] = Path(image_path)
            log.debug(f'Converted image path at index {i} to Path object: {image_paths[i]}')
        else:
            log.debug(f'Image path at index {i} is already a Path object: {image_path}')

        if not do_not_provision_paths:
            log.debug(f'Provisioning image path at index {i}...')
            image_paths[i] = provision_path(image_paths[i], do_not_convert=do_not_convert_paths, **kwargs)
            log.debug(f'Provisioned image path at index {i}: {image_paths[i]}')

    if threaded:
        return scan_images_threaded(
                log,
                scanned_images,
                image_paths,
                num_threads=num_threads,
                enable_progress_bar=prog_bar,
                prog_bar=tqdm(total=len(image_paths), desc='Scanning Images', unit='image')
                )

    if prog_bar:
        log.debug('Progress bar flag is set to True.')
        log.debug('Creating progress bar...')
        image_paths = tqdm(image_paths)
        log.debug('Progress bar created.')

    for image_path in image_paths:
        log.debug(f'Scanning image: {image_path}')

        try:

            result = analyze_image(image_path, base_url=base_url, do_not_provision=True)
            log.debug(f'Creating scanned image from result data: {result}')

            scanned_image = create_scanned_image(result)
            log.debug(f'Scanned image created: {scanned_image}')

        except Exception as e:
            log.warning(f'Failed to scan image: {image_path} {result if hasattr(locals(), "result") else ""}!',
                        exc_info=True)
            if e.__class__.__name__ == 'KeyboardInterrupt':
                raise e from e

            log.debug(f'Adding image ({image_path} to failed images list...')
            failed_images.append(image_path)
            continue

        log.debug(f'Adding scanned image ({image_path}) to scanned images collection...')
        scanned_images.add_image(scanned_image)

    scanned_images.finalize()
    return scanned_images


# TODO Rename this here and in `scan_images`
def scan_images_threaded(log, scanned_images, image_paths, num_threads=8, enable_progress_bar=False, prog_bar=None):
    log.debug('Threading flag is set to True.')
    log.debug('Creating queue...')
    queue = Queue()
    log.debug('Queue created.')

    log.debug('Creating worker threads...')
    workers = [Worker(queue, scanned_images, enable_progress_bar=enable_progress_bar,prog_bar=prog_bar) for _ in range(
            num_threads)]
    log.debug(f'{len(workers)} Worker threads created.')

    log.debug('Starting worker threads...')
    for worker in workers:
        worker.start()
    log.debug('Worker threads started.')

    log.debug('Adding image paths to queue...')
    for image_path in image_paths:
        queue.put(image_path)
    log.debug('Image paths added to queue.')

    log.debug('Waiting for queue to empty...')
    queue.join()
    log.debug('Queue emptied.')

    log.debug('Adding None to queue to signal end of processing...')
    for _ in range(num_threads):
        queue.put(None)
    log.debug('None added to queue.')

    log.debug('Waiting for worker threads to finish...')
    for worker in workers:
        worker.join()

    log.debug('Worker threads finished.')

    scanned_images.finalize()

    return scanned_images
