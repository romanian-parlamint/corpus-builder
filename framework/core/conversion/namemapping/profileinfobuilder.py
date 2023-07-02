"""Defines a class for building profile info from the name."""
from framework.core.conversion.namemapping.speakerinfo import SpeakerInfo
import logging


class ProfileInfoBuilder:
    """Builds the profile info from the name."""

    def __init__(self):
        """Create a new instance of the class."""
        pass

    def build_profile_info(self, speaker_name: str) -> SpeakerInfo:
        """Build a profile info instance from the speaker name.

        Parameters
        ----------
        speaker_name: str, required
            The full name of the speaker.

        Returns
        -------
        speaker_info: SpeakerInfo
            The speaker info built from name.
        """
        # Split the name by space; this way, if there are name parts that are
        # separated by a comma, those will be considered (as they should) a
        # single part of the name.
        name_parts = speaker_name.strip().split(' ')
        if len(name_parts) < 2:
            raise ValueError(
                f"Speaker name '{speaker_name}' should contain at least two parts."
            )

        logging.info("Building profile info from name '%s'.", speaker_name)
        # The simple case; assume that the speaker name is
        # in (first name, last name) format
        if len(name_parts) == 2:
            first_name, last_name = name_parts
            logging.info(
                "The name '%s' was split into first name = '%s', last name = '%s'.",
                speaker_name, [first_name], [last_name])
            return SpeakerInfo([first_name], [last_name])

        # Assume that the speaker name is
        # in (first name, middle name, last name) format
        if len(name_parts) == 3:
            first_name, middle_name, last_name = name_parts
            logging.info(
                "The name '%s' was split into first name = '%s', last name = '%s'.",
                speaker_name, [first_name, middle_name], [last_name])
            return SpeakerInfo([first_name, middle_name], [last_name])

        # Because having three first names is a rare occurence in Romania,
        # assume that the speaker has two first names and two last names
        if len(name_parts) == 4:
            first_name, middle_name, *last_name = name_parts
            logging.info(
                "The name '%s' was split into first name = '%s', last name = '%s'.",
                speaker_name, [first_name, middle_name], last_name)
            return SpeakerInfo([first_name, middle_name], last_name)

        # At this point the intuition tells that a person can have
        # three first names and two last names.
        if len(name_parts) == 5:
            logging.info(
                "The name '%s' was split into first name = '%s', last name = '%s'.",
                speaker_name, name_parts[:3], name_parts[3:])
            return SpeakerInfo(name_parts[:3], name_parts[3:])

        # At this point, God knows what is what in the name parts.
        # As such, we'll assume that:
        # - if the number of name parts is odd then out of 2n+1 parts,
        #   n+1 are the first name, and the rest are the last name;
        # - if the number of name parts is even then half of the
        #   name parts are the first name of the speaker, and the other
        #   half of the name parts are the last name.
        pivot = len(name_parts) // 2
        if len(name_parts) % 2 == 1:
            pivot = pivot + 1

        logging.info(
            "The name '%s' was split into first name = '%s', last name = '%s'.",
            speaker_name, name_parts[:pivot], name_parts[pivot:])
        return SpeakerInfo(name_parts[:pivot], name_parts[pivot:])
