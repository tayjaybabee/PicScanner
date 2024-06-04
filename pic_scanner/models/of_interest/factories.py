import json
from typing import Union

from pic_scanner.common.constants import LABEL_DESCRIPTIONS, VALID_LABELS
from pic_scanner.models.of_interest import OfInterest
from pic_scanner.models.of_interest.concern import Concern
from pic_scanner.models.of_interest.non_interesting import NonInteresting


class InterestFactory:
    """
    A InterestFactory that can be configured.

    Attributes:
        concerns:
            A list of labels that are concerning or might need special attention.

        points_of_interest:
            A list of labels that are points of interest. All labels are points of interest until they are marked as
            concerning.
    """

    concerns = []
    points_of_interest = []
    non_interesting = []
    for label in VALID_LABELS:
        points_of_interest.append(label)

    def __init__(self, all_non_interesting=False):
        """
        Initialize a new InterestFactory.

        Parameters:
            all_non_interesting (bool):
                A flag indicating whether all labels should be marked as non-interesting.

        Returns:
            None
        """
        if all_non_interesting:
            for label in VALID_LABELS:
                self.make_non_interesting(label)

    def mark(self, name, interest_level, case_sensitive=False):
        interest_levels = ['concerning', 'non_interesting', 'point_of_interest']
        if interest_level not in interest_levels:
            raise ValueError(f"Invalid interest level: {interest_level}!")

        if not case_sensitive:
            name = name.upper()

        if interest_level == 'concerning':
            self.remove_non_interesting(name, case_sensitive=case_sensitive)


    def make_concerning(self, name, case_sensitive=False):
        """
        Mark a label as concerning.

        Parameters:
            name (str):
                The name of the label to mark as concerning.

            case_sensitive (bool):
                A flag indicating whether the label name should be treated as case-sensitive.

        Returns:
            None
        """
        if not case_sensitive:
            name = name.upper()

        if 'GENITALIA_EXPOSED' in name:
            if 'MALE' in name or 'FEMALE' in name:
                self.points_of_interest.remove(name)
            else:
                names = ['MALE_GENITALIA_EXPOSED', 'FEMALE_GENITALIA_EXPOSED']
                for name in names:
                    self.points_of_interest.remove(name)
                    self.concerns.append(name)
                self.points_of_interest.remove('MALE_GENITALIA_EXPOSED')
            self.concerns.append(name)
        if name in self.points_of_interest:
            self.points_of_interest.remove(name)
            self.concerns.append(name)

    def make_non_interesting(self, name: str, case_sensitive=False):
        """
        Mark a label as non-interesting.

        Parameters:
            name (str):
                The name of the label to mark as non-interesting.

        Returns:
            None
        """
        if name in self.points_of_interest:
            self.points_of_interest.remove(name)
            self.non_interesting.append(name)

    def revert_to_point_of_interest(self, name):
        """
        Revert a label to a point of interest.

        Parameters:
            name (str):
                The name of the label to revert to a point of interest.

        Returns:
            None
        """
        if name in self.concerns:
            self.concerns.remove(name)
            self.points_of_interest.append(name)

    def get_concerns(self):
        """
        Get the list of concerns.

        Returns:
            list:
                The list of concerns.
        """
        return self.concerns

    def get_non_interesting(self):
        """
        Get the list of non-interesting labels.

        Returns:
            list:
                The list of non-interesting labels.
        """
        return self.non_interesting

    def get_points_of_interest(self):
        """
        Get the list of points of interest.

        Returns:
            list:
                The list of points of interest.
        """
        return self.points_of_interest

    def get_all_labels(self):
        """
        Get all labels.

        Returns:
            list:
                All labels.
        """
        return VALID_LABELS

    def get_interest_dict(self):
        """
        Get a dictionary of all labels and their status.

        Returns:
            dict:
                A dictionary of all labels and their status.
        """
        return {
            'concerns': self.concerns,
            'points_of_interest': self.points_of_interest,
            'non_interesting': self.non_interesting
        }

    def get_interest_dict_as_json(self):
        """
        Get a dictionary of all labels and their status as a JSON string.

        Returns:
            str:
                A JSON string of all labels and their status.
        """
        return json.dumps(self.get_interest_dict(), indent=4)

    def create(self, name, **kwargs) -> Union[OfInterest, Concern, NonInteresting]:
        """
        Create a new OfInterest object.

        Parameters:
            name (str):
                The name of the OfInterest object to create.

        Returns:
            OfInterest:
                The OfInterest object.
        """
        if name in self.concerns:
            return Concern(name, **kwargs)
        elif name in self.non_interesting:
            return NonInteresting(name, **kwargs)
        else:
            return OfInterest(name, **kwargs)

    def remove_concerning(self, name, case_sensitive=False):
        if not case_sensitive:
            name = name.upper()

        self.concerns.remove(name)
        self.points_of_interest.append(name)

    def remove_non_interesting(self, name, case_sensitive=False):
        if not case_sensitive:
            name = name.upper()

        self.non_interesting.remove(name)
        self.points_of_interest.append(name)

    def move_from_points_of_interest(self, name, to):
        if name not in self.points_of_interest:
            raise ValueError(f"Label {name} is not in points of interest!")

        self.points_of_interest.remove(name)

        if to == 'concerning':
            self.concerns.append(name)
        elif to == 'non_interesting':
            self.non_interesting.append(name)
        else:
            raise ValueError(f"Invalid interest level: {to}!")
