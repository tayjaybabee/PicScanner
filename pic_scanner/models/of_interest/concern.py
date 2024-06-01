from pic_scanner.log_engine import Loggable
from pic_scanner.models.of_interest import MOD_LOGGER as PARENT_LOGGER


MOD_LOGGER = PARENT_LOGGER.get_child('concern')


class Concern(Loggable, OfInterest):
    """
    A class detailing a NSFW concern (or 'detection') found on an image.

    Attributes:
        name: The name of the concern.
        score: The score of the concern.
        location: The location of the concern.
        description: The description of the concern.
    """
