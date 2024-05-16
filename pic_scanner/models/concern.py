from typing import Optional
from inspyre_toolbox.syntactic_sweets.properties.descriptors import RestrictedSetter


__all__ = [
    'Concern'
]


class Concern:
    """
    A class detailing a NSFW concern (or 'detection') found on an image.

    Attributes:
        name: The name of the concern.
        score: The score of the concern.
        location: The location of the concern.
        description: The description of the concern.
    """
    name = RestrictedSetter(
        'name',
        allowed_types=str,
        restrict_setter=True
    )

    score = RestrictedSetter(
        'score',
        allowed_types=float,
        restrict_setter=True
    )

    location = RestrictedSetter(
        'location',
        allowed_types=list,
        restrict_setter=True
    )

    description = RestrictedSetter(
        'description',
        allowed_types=(str, type(None)),
        restrict_setter=True
    )

    def __init__(self, name: str, score: float, location: list[int], description: Optional[str] = None):
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

        Raises:
            TypeError:
                If the name is not a string.

            TypeError:
                If the score is not a float.

            TypeError:
                If the location is not a list of integers.

            TypeError:
                If the description is not a string or None.

        Examples:
            >>> concern = Concern('NSFW', 0.9, [0, 0, 100, 100], 'NSFW content detected.')
        """
        self.name = name
        self.score = score
        self.location = location
        self.description = description

    def __str__(self):
        """
        Return a string representation of the concern.

        Returns:
            str:
                The string representation of the concern.
        """
        return f'{self.name} ({self.score}) at {self.location}'

    def __repr__(self):
        """
        Return a string representation of the concern.

        Returns:
            str:
                The string representation of the concern.
        """
        return f'Concern({self.name}, {self.score}, {self.location}, {self.description})'

