from pic_scanner.log_engine import Loggable
from pic_scanner.models.of_interest import MOD_LOGGER as PARENT_LOGGER, OfInterest
from typing import Optional


MOD_LOGGER = PARENT_LOGGER.get_child('concern')


class Concern(OfInterest):
    """
    A class detailing a NSFW concern (or 'detection') found on an image.

    Attributes:
        name: The name of the concern.
        score: The score of the concern.
        location: The location of the concern.
        description: The description of the concern.
    """
    def __init__(
            self,
            name: str,
            score: float,
            location: list[int],
            description: Optional[str] = None
            ) -> None:
        """
        Initialize a new concern.

        Parameters:
            name (str):
                The name of the concern.

            score (float):
                The score of the concern.

            location (list[int]):
                The location of the concern.

            description (Optional[str]):
                The description of the concern.

        Returns:
            None
        """
        super().__init__(name, score, location, description)
        self.logger = self.log_device.get_child('Concern')

        self.logger.debug(f'Concern created: {self}')
