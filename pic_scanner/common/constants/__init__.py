"""
__init__.py

This module contains constants and default settings used across the application.

Imports:
    from .defaults import *
    from .meta.constants import *

Constants:
    AUTHORS (list): A list of authors of the project.
    DEFAULT_BASE_URL (str): The default base URL for the API.
    FILE_SYSTEM_DEFAULTS (dict): Default settings for the file system.
    IMAGE_EXTENSIONS (list): A list of valid image extensions.
    LABEL_DESCRIPTIONS (dict): A dictionary containing labels and their descriptions.
    PROG_NAME (str): The name of the program.
    RELEASE_MAP (dict): A mapping of releases.
    UNIT_ABBREVIATION_MAP (dict): A dictionary that maps unit abbreviations to their full names.
    URLS (dict): A dictionary containing various URLs used in the application.
    VALID_LABELS (set): A set of valid labels that can be used to classify images in the dataset.
    VERSION (str): The version of the program.

Attributes:
    UNIT_ABBREVIATION_MAP (dict): A dictionary that maps unit abbreviations to their full names.
        Example:
            {
                'B': 'bytes',
                'KB': 'kilobytes',
                'MB': 'megabytes',
                'GB': 'gigabytes',
                'TB': 'terabytes',
                'PB': 'petabytes',
                'EB': 'exabytes',
                'ZB': 'zetabytes',
                'YB': 'yottabytes',
            }

    DEFAULT_BASE_URL (str): The default base URL for the API.
        Example: 'http://localhost:8080/infer'

    LABEL_DESCRIPTIONS (dict): A dictionary that contains the labels and their descriptions.
        Example:
            {
                "FEMALE_GENITALIA_COVERED": "Female genitalia covered",
                "FACE_FEMALE":              "Female face",
                "BUTTOCKS_EXPOSED":         "Exposed buttocks",
                "FEMALE_BREAST_EXPOSED":    "Exposed female breasts",
                "FEMALE_GENITALIA_EXPOSED": "Exposed female genitalia",
                "MALE_BREAST_EXPOSED":      "Exposed male breasts",
                "ANUS_EXPOSED":             "Exposed anus",
                "FEET_EXPOSED":             "Exposed feet",
                "BELLY_COVERED":            "Covered belly",
                "FEET_COVERED":             "Covered feet",
                "ARMPITS_COVERED":          "Covered armpits",
                "ARMPITS_EXPOSED":          "Exposed armpits",
                "FACE_MALE":                "Male face",
                "BELLY_EXPOSED":            "Exposed belly",
                "MALE_GENITALIA_EXPOSED":   "Exposed male genitalia",
                "ANUS_COVERED":             "Covered anus",
                "FEMALE_BREAST_COVERED":    "Covered female breasts",
                "BUTTOCKS_COVERED":         "Covered buttocks",
            }

    VALID_LABELS (set): A set of valid labels that can be used to classify images in the dataset.
        Example:
            {"FEMALE_GENITALIA_COVERED", "FACE_FEMALE", "BUTTOCKS_EXPOSED", ...}

    IMAGE_EXTENSIONS (list): A list of valid image extensions.
        Example: ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
"""

from .defaults import *
from ..meta.constants import *

__all__ = [
        'AUTHORS',
        'DEFAULT_BASE_URL',
        'FILE_SYSTEM_DEFAULTS',
        'IMAGE_EXTENSIONS',
        'LABEL_DESCRIPTIONS',
        'PROG_NAME',
        'RELEASE_MAP',
        'UNIT_ABBREVIATION_MAP',
        'URLS',
        'VALID_LABELS',
        'VERSION',
        ]


UNIT_ABBREVIATION_MAP = {
    'B': 'bytes',
    'KB': 'kilobytes',
    'MB': 'megabytes',
    'GB': 'gigabytes',
    'TB': 'terabytes',
    'PB': 'petabytes',
    'EB': 'exabytes',
    'ZB': 'zetabytes',
    'YB': 'yottabytes',
        }
"""
dict:
    A dictionary that maps unit abbreviations to their full names.
"""


DEFAULT_BASE_URL = 'http://localhost:8080/infer'
"""
str:
    The default base URL for the API.
"""


LABEL_DESCRIPTIONS = {
            "FEMALE_GENITALIA_COVERED": "Female genitalia covered",
            "FACE_FEMALE":              "Female face",
            "BUTTOCKS_EXPOSED":         "Exposed buttocks",
            "FEMALE_BREAST_EXPOSED":    "Exposed female breasts",
            "FEMALE_GENITALIA_EXPOSED": "Exposed female genitalia",
            "MALE_BREAST_EXPOSED":      "Exposed male breasts",
            "ANUS_EXPOSED":             "Exposed anus",
            "FEET_EXPOSED":             "Exposed feet",
            "BELLY_COVERED":            "Covered belly",
            "FEET_COVERED":             "Covered feet",
            "ARMPITS_COVERED":          "Covered armpits",
            "ARMPITS_EXPOSED":          "Exposed armpits",
            "FACE_MALE":                "Male face",
            "BELLY_EXPOSED":            "Exposed belly",
            "MALE_GENITALIA_EXPOSED":   "Exposed male genitalia",
            "ANUS_COVERED":             "Covered anus",
            "FEMALE_BREAST_COVERED":    "Covered female breasts",
            "BUTTOCKS_COVERED":         "Covered buttocks",
}
"""
dict:
    A dictionary that contains the labels and their descriptions.
    
    The keys are the labels and the values are the descriptions.
"""


VALID_LABELS = set(LABEL_DESCRIPTIONS.keys())
"""
set:
    A set of valid labels that can be used to classify images in the dataset.
"""

IMAGE_EXTENSIONS = [
    '.png',
    '.jpg',
    '.jpeg',
    '.bmp',
    '.tiff'
    ]
"""
list:
    A list of valid image extensions.
"""
