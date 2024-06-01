from typing import Optional

from inspyre_toolbox.syntactic_sweets.properties import RestrictedSetter, validate_type
from inspyre_toolbox.syntactic_sweets.properties.descriptors import RestrictedSetter
from inspyre_toolbox.syntactic_sweets.properties.decorators import validate_type

from pic_scanner.common import LABEL_DESCRIPTIONS, VALID_LABELS
from pic_scanner.common.constants import VALID_LABELS, LABEL_DESCRIPTIONS
from pic_scanner.helpers.properties import validate_float_between
from pic_scanner.log_engine import Loggable
from pic_scanner.models import MOD_LOGGER as PARENT_LOGGER


MOD_LOGGER = PARENT_LOGGER.get_child('concern')


__all__ = [
        'OfInterest'
]


class OfInterest:
    description = RestrictedSetter(
        'description',
        allowed_types=(str, type(None)),
        restrict_setter=True
    )
    location = RestrictedSetter(
        'location',
        allowed_types=list,
        restrict_setter=True
    )
    score = RestrictedSetter(
        'score',
        allowed_types=float,
        restrict_setter=True
    )
    name = RestrictedSetter(
        'name',
        allowed_types=str,
        restrict_setter=True
    )

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
        super().__init__(parent_log_device=MOD_LOGGER)
        self.__description = None
        self.__location = None
        self.__name = None
        self.__score = None

        log = self.log_device

        self.name = name
        log.debug(f'Concern name set to: {self.name}')

        self.score = score
        log.debug(f'Concern score set to: {self.score}')

        self.location = location
        log.debug(f'Concern location set to: {self.location}')

        self.description = description or LABEL_DESCRIPTIONS.get(name, None)
        log.debug(f'Concern description set to: {self.description}')

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

    @property
    def score_percentage(self) -> float:
        """
        Return the score of the concern as a percentage.

        Returns:
            float:
                The score of the concern as a percentage.
        """
        return self.score * 100

    @property
    def score(self) -> float:
        """
        Return the score of the concern.

        Returns:
            float:
                The score of the concern.
        """
        return self.__score

    @score.setter
    @validate_float_between()
    def score(self, value: float):
        """
        Set the score of the concern.

        Parameters:
            value (float):
                The score of the concern.

        Returns:
            None

        Raises:
            TypeError:
                If the value is not a float.

            ValueError:
                If the value is not between 0.0 and 1.0.
        """
        self.__score = value

    @property
    def score_percentage_str(self) -> str:
        """
        Return the score of the concern as a percentage string.

        Returns:
            str:
                The score of the concern as a percentage string.
        """
        return f'{self.score_percentage:.2f}%'

    @property
    def name(self) -> str:
        """
        Return the name of the concern.

        Returns:
            str:
                The name of the concern.
        """
        return self.__name

    @name.setter
    @validate_type(str, allowed_values=VALID_LABELS)
    def name(self, value: str):
        """
        Set the name of the concern.

        Parameters:
            value (str):
                The name of the concern.

        Returns:
            None

        Raises:
            TypeError:
                If the value is not a string.

            ValueError:
                If the value is not a valid label.
        """
        self.__name = value

    @property
    def description(self) -> Optional[str]:
        """
        Return the description of the concern.

        Returns:
            Optional[str]:
                The description of the concern.
        """
        return self.__description

    @description.setter
    @validate_type(str, allowed_values=LABEL_DESCRIPTIONS.values())
    def description(self, value: Optional[str]):
        """
        Set the description of the concern.

        Parameters:
            value (Optional[str]):
                The description of the concern.

        Returns:
            None

        Raises:
            TypeError:
                If the value is not a string or None.

            ValueError:
                If the value is not a valid description.
        """
        self.__description = value

    @property
    def location(self) -> list[int]:
        """
        Return the location of the concern.

        Returns:
            list[int]:
                The location of the concern.
        """
        return self.__location

    @location.setter
    @validate_type(list)
    def location(self, value: list[int]):
        """
        Set the location of the concern.

        Parameters:
            value (list[int]):
                The location of the concern.

        Returns:
            None

        Raises:
            TypeError:
                If the value is not a list of integers.
        """
        self.__location = value
