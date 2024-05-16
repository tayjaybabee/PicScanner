"""
A module containing classes and functions for image processing, loading, and saving.
"""
from pathlib import Path
from typing import Union
from warnings import warn
from inspyre_toolbox.syntactic_sweets.properties.descriptors import RestrictedSetter
from inspyre_toolbox.syntactic_sweets.properties.decorators import validate_type

from shutil import copy as copy_file

from ..common.constants import LABEL_DESCRIPTIONS
from .concern import Concern
from ..helpers.filesystem import provision_path


__all__ = [
    'ScannedImage',
    'ScannedImageCollection',
    'create_scanned_image',
    'get_description',

]


def get_description(class_name):
    """
    Get the description of a label.

    Parameters:
        class_name (str):
            The name of the label.

    Returns:
        str:
            The description of the label.
    """
    return LABEL_DESCRIPTIONS[class_name.upper()]


class ScannedImage:
    """
    A class representing a scanned image.

    Properties:
        image_path (str, Path):
            The path of the image.

        backed_up (bool):
            The backup status of the image.

        concerns (list):
            The list of concerns associated with the image.

        concern_count (int):
            The number of concerns associated with the image.

        concern_names (list):
            The names of the concerns associated with the image.

    Methods:
        add_concern(concern):
            Add a concern to the scanned image.

        backup(backup_dir, backup_name, **kwargs):
            Backup the image.

        create_concerns(result):
            Create concerns from a result dictionary.

        get_concerns():
            Get the concerns associated with the image.

        get_concerns_by_name(name):
            Get the concerns associated with the image by name.

        has_concern(name, case_sensitive):
            Check if the image has a concern.

        move(new_dir, new_name):
            Move the image to a new directory.
    """

    image_path = RestrictedSetter(
        'image_path',
        allowed_types=(str, Path),
        preferred_type=Path,
        restrict_setter=True,
    )

    def __init__(self, image_path: Union[str, Path]):
        """
        The constructor for ScannedImage class.

        Parameters:
            image_path (str, Path): The path of the image.
        """
        self.__backed_up = False
        self.__concerns = []

        self.image_path = image_path


    @property
    def backed_up(self) -> bool:
        """
        Get the backed up status of the image.

        Returns:
            bool:
                The backed up status of the image.
        """
        return self.__backed_up

    @property
    def concerns(self):
        """
        Get the concerns associated with the image.

        Returns:
            list:
                The concerns associated with the image.
        """
        return self.__concerns

    @property
    def concern_count(self):
        """
        Get the number of concerns associated with the image.

        Returns:
            int:
                The number of concerns associated with the image.
        """
        return len(self.__concerns)

    @property
    def concern_names(self):
        """
        Get the names of the concerns associated with the image.

        Returns:
            list:
        """
        return [concern.name for concern in self.concerns]

    def add_concern(self, concern):
        """
        Add a concern to the scanned image.

        Parameters:
            concern (Concern):
                The concern to add to the scanned image.

        Returns:
            None
        """
        if not isinstance(concern, Concern):
            raise ValueError(f"The concern must be an instance of the Concern class, not {type(concern)}!"
                             f"")
        self.__concerns.append(concern)

    def backup(self, backup_dir=None, backup_name=None, **kwargs):
        """
        Backup the scanned image.

        Parameters:
            backup_dir (str, Path):
                The directory to store the backup.

            backup_name (str):
                The name of the backup file.

        Returns:
            Path:
                The path of the backup file.
        """
        if backup_dir is None:
            backup_dir = self.image_path.parent / 'backups'

        backup_dir = provision_path(backup_dir, **kwargs)

        if backup_name is None:
            backup_name = f'{self.image_path.name}_backup'

        backup_path = backup_dir / backup_name

        copy_file(self.image_path, backup_path)

        return backup_path

    def create_concerns(self, result):
        """
        Create concerns from a result dictionary.

        Parameters:
            result (dict):
                The result dictionary.

        Returns:
            None
        """
        result = result['result']

        detections = result.get('prediction', [])

        for detection_list in detections:
            for detection in detection_list:
                class_name = detection.get('class')
                score = detection.get('score')
                location = detection.get('box')
                description = get_description(class_name)
                if description:
                    self.add_concern(Concern(class_name, score, location, description))

    def get_concerns(self):
        """
        Get the concerns associated with the image.

        Returns:
            list:
                The concerns associated with the image.
        """
        return self.concerns

    def get_concerns_by_name(self, name):
        """
        Get the concerns associated with the image by name.

        Parameters:
            name (str):
                The name of the concern.

        Returns:
            list:
                The concerns associated with the image by name.
        """
        concerns = []
        for concern in self.__concerns:
            if concern.name == name:
                concerns.append(concern)
        return concerns

    def has_concern(self, name, case_sensitive=False):
        """
        Check if the image has a concern by name.

        Parameters:
            name (str): The name of the concern.
            case_sensitive (bool): If the check should be case sensitive.

        Returns:
            bool:
                True if the image has the concern, False otherwise.
        """
        if case_sensitive:
            return name in self.concern_names

        if name.upper() in self.concern_names:
            return True

    def move(self, new_dir, new_name=None):
        """
        Move the image to a new directory.

        Parameters:
            new_dir (str):
                The new directory to move the image to.

            new_name (str):
                The new name of the image.

        Returns:
            None
        """
        new_dir = Path(new_dir)
        new_dir.mkdir(parents=True, exist_ok=True)
        new_name = new_name or self.image_path.name
        new_path = new_dir / new_name
        self.image_path.rename(new_path)
        self.image_path = new_path


class ScannedImageCollection:
    """
    A class representing a collection of scanned images.

    Properties:
        images (list):
            The list of scanned images.

        concern_names (list):
            The names of the concerns associated with the images in the collection.

        concerns (list):
            The concerns associated with the images in the collection.

        concern_count (int):
            The number of concerns associated with the images in the collection.

        image_count (int):
            The number of images in the collection.

        image_paths (list):
            The paths of the images in the collection.
    """

    RestrictedSetter(
        'images',
        allowed_types=list,
        restrict_setter=True,
        initial=[]
    )

    def __init__(self):
        """
        The constructor for ScannedImageCollection class.
        """
        self.images = []

    def add_image(self, image: ScannedImage):
        """
        Add a scanned image to the collection.

        Parameters:
            image (ScannedImage):
                The scanned image to add to the collection.

        Returns:
            None
        """
        if not isinstance(image, ScannedImage):
            raise ValueError(f"The image must be an instance of the ScannedImage class, not {type(image)}!")

        self.images.append(image)

    def remove_image(self, image):
        """
        Remove a scanned image from the collection.

        Parameters:
            image (ScannedImage):
                The scanned image to remove from the collection.

        Returns:
            None
        """

        if image in self.images:
            self.images.remove(image)
        else:
            raise ValueError(f"The image {image} is not in the collection!")

    def get_all_with_concern(self, concern_name: str, case_sensitive=False):
        """
        Get all images with a specific concern.

        Parameters:
            concern_name (str):
                The name of the concern.

            case_sensitive (bool):
                If the check should be case-sensitive.

        Returns:
            list:
                A list of images with the concern.
        """
        images = []

        if not case_sensitive:
            concern_name = concern_name.upper()

        if concern_name not in self.concern_names:
            warn(f"The concern {concern_name} is not in the collection!")
        else:
            for image in self.images:
                if image.has_concern(concern_name, case_sensitive):
                    images.append(image)
            return images

    def get_image(self, image_path):
        """
        Get a scanned image from the collection by path.

        Parameters:
            image_path (str, Path):
                The path of the scanned image.

        Returns:
            ScannedImage:
                The scanned image.
        """
        for image in self.images:
            if image.image_path == image_path:
                return image
        raise ValueError(f"The image {image_path} is not in the collection!")

    def get_concerns(self):
        """
        Get the concerns associated with the images in the collection.

        Returns:
            list:
                The concerns associated with the images in the collection.
        """
        concerns = set()
        for image in self.images:
            for concern in image.concerns:
                concerns.add(concern)
        return list(concerns)

    def get_concerns_by_name(self, name):
        """
        Get the concerns associated with the images in the collection by name.

        Parameters:
            name (str):
                The name of the concern.

        Returns:
            list:
                The concerns associated with the images in the collection by name.
        """
        concerns = []
        for image in self.images:
            for concern in image.__concerns:
                if concern.name == name:
                    concerns.append(concern)
        return concerns

    def get_concerns_by_score(self, score):
        """
        Get concerns by score.

        Parameters:
            score:
                The score of the concern.

        Returns:
            list:
                A list of concerns with the given score.
        """
        concerns = []
        for image in self.images:
            for concern in image.__concerns:
                if concern.score == score:
                    concerns.append(concern)
        return concerns

    def get_concern_names(self):
        """
        Get the names of the concerns associated with the images in the collection.

        Returns:
            list:
                The names of the concerns associated with the images in the collection.
        """
        names = set()
        for image in self.images:
            for concern in image.concerns:
                names.add(concern.name)

        return list(names)

    def move_all_with_concern(self, new_dir, concern_name):
        """
        Move all images with a specific concern to a new directory.

        Parameters:
            new_dir (str, Path):
                The new directory to move the images to.

            concern_name (str):
                The name of the concern.

        Returns:
            None
        """
        for image in self.images:
            if concern_name in image.concern_names:
                image.move(new_dir)

    @property
    def concern_names(self):
        """
        Get the names of the concerns associated with the images in the collection.

        Returns:
            list:
                The names of the concerns associated with the images in the collection.
        """
        return self.get_concern_names()

    @property
    def concerns(self):
        """
        Get the concerns associated with the images in the collection.

        Returns:
            list:
                The concerns associated with the images in the collection.
        """
        return self.get_concerns()

    @property
    def concern_count(self):
        """
        Get the number of concerns associated with the images in the collection.

        Returns:
            int:
                The number of concerns associated with the images in the collection.
        """
        return len(self.concerns)

    @property
    def image_count(self):
        """
        Get the number of images in the collection.

        Returns:
            int:
                The number of images in the collection.
        """
        return len(self.images)

    @property
    def image_paths(self):
        """
        Get the paths of the images in the collection.

        Returns:
            list:
                The paths of the images in the collection.
        """
        return [image.image_path for image in self.images]



def create_scanned_image(result_struct):
    """
    Create a scanned image from a result dictionary.

    Parameters:
        result_struct (dict):
            The result dictionary.

    Returns:
        ScannedImage:
            The scanned image.
    """
    image_path = result_struct['image_path']
    scanned_image = ScannedImage(image_path)
    scanned_image.create_concerns(result_struct)
    return scanned_image
