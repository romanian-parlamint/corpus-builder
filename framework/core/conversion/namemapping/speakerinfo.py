"""Defines a class for representing speaker info."""
from typing import List


class SpeakerInfo:
    """Represents information about the speaker."""

    def __init__(self,
                 first_name: List[str],
                 last_name: List[str],
                 speaker_id: str = None,
                 sex: str = "U",
                 profile_image: str = None):
        """Create a new instance of the class.

        Parameters
        ----------
        first_name: list of str, required
            The parts of the first name.
        last_name: list of str, required
            The parts of the last name.
        speaker_id: str, optional
            The id of the speaker.
        sex: str, optional
            The sex of the speaker. Default value is U which means unknown.
        profile_image: str, optional
            The URL of the profile image.
        """
        self.__translations = str.maketrans({'Ş': 'Ș', 'ş': 'ș'})
        self.__first_name = self.__translate_name(first_name)
        self.__last_name = self.__translate_name(last_name)
        self.__speaker_id = None
        self.__sex = 'U'
        self.__profile_image = None
        # Set the properties
        self.speaker_id = speaker_id
        self.sex = sex
        self.profile_image = profile_image

    @property
    def profile_image(self) -> str:
        """Get the profile image URL.

        Returns
        -------
        profile_image: str
            The URL of the profile image.
        """
        return self.__profile_image

    @profile_image.setter
    def profile_image(self, value: str):
        """Set the profile image.

        Parameters
        ----------
        value: str, required
            The URL of the profile image.
        """
        self.__profile_image = value

    @property
    def sex(self) -> str:
        """Get the sex of the speaker.

        Returns
        -------
        sex: one of [M, F, U]
            The sex of the speaker: M(ale), F(emale), or U(nknown).
        """
        return self.__sex

    @sex.setter
    def sex(self, value: str):
        """Set the sex of the speaker.

        Parameters
        ----------
        value: str, one of [M, F, U], required
            The sex of the speaker.
        """ ""
        if value not in ['M', 'F', 'U']:
            raise ValueError("Sex must be one of 'M','F', or 'U'.")
        self.__sex = value

    @property
    def speaker_id(self) -> str:
        """Get the speaker id.

        Returns
        -------
        speaker_id: str
            The id of the speaker.
        """
        return self.__speaker_id

    @speaker_id.setter
    def speaker_id(self, value: str):
        """Set the speaker id.

        Parameters
        ----------
        value: str, required
            The speaker id.
        """
        self.__speaker_id = value

    @property
    def last_name(self) -> List[str]:
        """Get the last name.

        Returns
        -------
        last_name: list of str
            The parts of last name.
        """
        return self.__last_name

    @property
    def first_name(self) -> List[str]:
        """Get the first name.

        Returns
        -------
        first_name: list of str
            The parts of first name.
        """
        return self.__first_name

    def __translate_name(self, name: List[str]) -> List[str]:
        """Replace invalid characters in name.

        Parameters
        ----------
        name: list of str, required
            The name to translate.

        Returns
        -------
        translated_name: list of str
            The name with translated characters.
        """ ""
        return [p.translate(self.__translations) for p in name]
