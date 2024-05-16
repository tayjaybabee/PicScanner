
from .defaults import *


UNIT_ABBREBIATION_MAP = {
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



DEFAULT_BASE_URL = 'http://localhost:8080/infer'
"""
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
The keys are the labels that are used in the dataset. The values are the descriptions of the labels.

The labels are used to classify the images in the dataset.
"""


VALID_LABELS = set(LABEL_DESCRIPTIONS.keys())
"""
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
A list of valid image extensions.
"""


__all__ = [
        'DEFAULT_BASE_URL',
        'LABEL_DESCRIPTIONS',
        'VALID_LABELS',
        'IMAGE_EXTENSIONS',
        ]
