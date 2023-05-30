"""Defines a class to resolve speaker info from speaker name."""
from framework.core.conversion.namemapping.speakerinfo import SpeakerInfo
from typing import Iterable
from typing import List
from unidecode import unidecode


class SpeakerInfoResolver:
    """Provides speaker info for the specified name."""

    def __init__(self, speaker_data: Iterable[SpeakerInfo]):
        """Create a new instance of the class.

        Parameters
        ----------
        speaker_data: iterable of SpeakerInfo, required
            The collection of speaker information.
        """
        self.__speaker_data = {
            self.__build_speaker_info_search_key(info): info
            for info in speaker_data
        }

    def resolve(self, full_name: str) -> SpeakerInfo | None:
        """Resolve the profile info from the full name of the speaker.

        Parameters
        ----------
        full_name: str, required
            The full name of the speaker.

        Returns
        -------
        speaker_info: SpeakerInfo
            The speaker info if found; None otherwise.
        """
        key = self.__build_full_name_search_key(full_name)
        if key in self.__speaker_data:
            return self.__speaker_data[key]

        return None

    def __build_speaker_info_search_key(self,
                                        speaker_info: SpeakerInfo) -> str:
        """Build a search key from the speaker info.

        Parameters
        ----------
        speaker_info: SpeakerInfo, required
            The speaker info from which to build the key.

        Returns
        -------
        key: str
            The search key.
        """
        name_tokens, name_parts = [], speaker_info.first_name + speaker_info.last_name
        for name_part in name_parts:
            name_tokens.extend(self.__tokenize_name(name_part))
        return self.__build_search_key(name_tokens)

    def __build_full_name_search_key(self, full_name: str) -> str:
        """Build a search key from the full name of the speaker.

        Parameters
        ----------
        full_name: str, required
            The full name of the speaker.

        Returns
        -------
        key: str
            The search key.
        """
        name_tokens = self.__tokenize_name(full_name)
        return self.__build_search_key(name_tokens)

    def __build_search_key(self, tokens: List[str]) -> str:
        """Build the search key from the provided tokens.

        Parameters
        ----------
        tokens: list of str, required
            The tokens from which to build the search key.

        Returns
        -------
        key: str
            The search key.
        """
        return '-'.join(sorted(tokens))

    def __tokenize_name(self, name: str) -> List[str]:
        """Tokenize the name.

        Parameters
        ----------
        name: str, required
            The name to tokenize.

        Returns
        -------
        tokens: list of str
            The tokens of the name.
        """
        name = unidecode(name.lower())
        name = name.replace('-', ' ')
        name = name.strip()
        return [tok.strip() for tok in name.split(' ') if len(tok.strip()) > 0]
