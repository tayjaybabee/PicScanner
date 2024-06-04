Using the PicScanner Library
============================

Overview
--------

The PicScanner library provides functionality for scanning images for NSFW content. This document describes how to use the `scan_image` and `scan_images` functions to perform these scans.

Functions
---------

scan_image
~~~~~~~~~~

Scan a single image for NSFW content.

**Parameters**

- `image_path` (Union[str, Path]): The path to the image to scan.
- `base_url` (Optional[str]): The base URL of the API to use.

**Returns**

- `ScannedImage`: The scanned image.

**Raises**

- `ValueError`: If the image path is invalid.

**Example Usage**

.. code-block:: python

    from pic_scanner.core import scan_image
    from pathlib import Path

    image_path = Path("/path/to/your/image.jpg")
    scanned_image = scan_image(image_path)

scan_images
~~~~~~~~~~~

Scan a collection of images for NSFW content.

**Parameters**

- `image_paths` (Union[list[Union[str, Path]], Path]): The paths to the images to scan.
- `base_url` (Optional[str]): The base URL of the API to use.
- `do_not_convert_paths` (bool): A flag indicating whether to convert the paths to strings.
- `do_not_provision_paths` (bool): A flag indicating whether to provision the paths.
- `prog_bar` (bool): A flag indicating whether to display a progress bar.
- `threaded` (bool): A flag indicating whether to use threading for the scanning process.
- `num_threads` (int): The number of threads to use if threading is enabled.

**Returns**

- `ScannedImageCollection`: The scanned images.

**Raises**

- `ValueError`: If the image paths are invalid.

**Example Usage**

.. code-block:: python

    from pic_scanner.core import scan_images
    from pathlib import Path

    image_paths = [Path("/path/to/your/image1.jpg"), Path("/path/to/your/image2.jpg")]
    scanned_images = scan_images(image_paths, prog_bar=True, threaded=True, num_threads=4)

Classes
-------

Worker
~~~~~~

A worker thread for processing images.

**Parameters**

- `queue` (Queue): The queue of image paths to process.
- `collection` (ScannedImageCollection): The collection to store scanned images.
- `enable_progress_bar` (bool): A flag indicating whether to enable the progress bar.
- `prog_bar` (tqdm): The progress bar object.

**Methods**

- `run()`: The main method to process images from the queue.

**Example Usage**

.. code-block:: python

    from pic_scanner.core import Worker
    from queue import Queue
    from pic_scanner.models.image import ScannedImageCollection

    queue = Queue()
    collection = ScannedImageCollection()
    worker = Worker(queue, collection, enable_progress_bar=True, prog_bar=tqdm(total=10))
    worker.start()

Notes
-----

- The `scan_image` function provides a simple interface for scanning a single image, while `scan_images` allows for batch processing with optional threading and progress indication.
- The `Worker` class is used internally by `scan_images` when threading is enabled.

For further details and advanced usage, refer to the source code and additional documentation provided in the PicScanner repository.
