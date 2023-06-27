"""Defines a class for building speaker id."""
from unidecode import unidecode
import re


class SpeakerIdBuilder:
    """Builds speaker id."""

    def __init__(self):
        """Create a new instance of the class."""
        self.__id_translations = str.maketrans({' ': '-'})

    def build_speaker_id(self, full_name: str) -> str:
        """Build the speaker id from full name.

        Parameters
        ----------
        full_name: str, required
            The full name of the speaker.

        Returns
        -------
        speaker_id: str
            The id of the speaker.
        """
        canonical_id = full_name.translate(self.__id_translations)
        canonical_id = re.sub(r"-{2,}", '-', canonical_id)
        return f'#{unidecode(canonical_id)}'
