from pic_scanner.models.of_interest import MOD_LOGGER as PARENT_LOGGER, Loggable, OfInterest


MOD_LOGGER = PARENT_LOGGER.get_child('non_interesting')


class NonInteresting(Loggable, OfInterest):
    """
    A class detailing a non-interesting label found on an image.

    Attributes:
        name: The name of the non-interesting label.
        score: The score of the non-interesting label.
        location: The location of the non-interesting label.
        description: The description of the non-interesting label.
    """
    def __init__(
            self,
            name: str,
            score: float,
            location: list[int],
            description: str = None
            ) -> None:
        """
        Initialize a new non-interesting label.

        Parameters:
            name (str):
                The name of the non-interesting label.

            score (float):
                The score of the non-interesting label.

            location (list[int]):
                The location of the non-interesting label.

            description (Optional[str]):
                The description of the non-interesting label.

        Returns:
            None
        """
        OfInterest.__init__(self, name, score, location, description)
        Loggable.__init__(self, MOD_LOGGER)
        self.logger.debug(f'Non-interesting label created: {self}')
