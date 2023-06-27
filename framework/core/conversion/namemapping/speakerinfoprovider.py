"""Defines class for providing speaker info."""
from framework.core.conversion.namemapping.speakerinfo import SpeakerInfo
from framework.core.conversion.namemapping.speakernameresolver import SpeakerNameResolver
from framework.core.conversion.namemapping.speakerinforesolver import SpeakerInfoResolver
from framework.core.conversion.namemapping.speakeridbuilder import SpeakerIdBuilder
from framework.core.conversion.namedtuples import NameCorrection
from typing import List
import logging


class SpeakerInfoProvider:
    """Provides speaker info."""

    EMPTY_SPEAKER = SpeakerInfo(['Necunoscut'], ['Necunoscut'],
                                speaker_id="Necunoscut-Necunoscut")

    def __init__(self, name_corrections: List[NameCorrection],
                 personal_info: List[SpeakerInfo]):
        """Create a new instance of the class.

        Parameters
        ----------
        name_corrections: list of NameCorrection, required
            The list of name corrections that map names as they appear in JSON transcriptions to correct names of speakers.
        personal_info: list of SpeakerInfo, required
            The list with personal info of the speakers.
        """
        self.__id_map = {}
        self.__id_builder = SpeakerIdBuilder()
        self.__name_resolver = SpeakerNameResolver(name_corrections)
        self.__info_resolver = SpeakerInfoResolver(personal_info)

    def get_speaker_id(self, speaker_name: str) -> str:
        """Get the speaker id from the provided full name of the speaker.

        Parameters
        ----------
        speaker_name: str, required
            The full name of the speaker.

        Returns
        -------
        speaker_id: str
            The id of the speaker.
        """
        actual_name = self.get_speaker_name(speaker_name)
        speaker_id = self.__id_builder.build_speaker_id(actual_name)
        self.__id_map[speaker_id] = actual_name
        return speaker_id

    def get_personal_info(self, speaker_id: str) -> dict:
        """Get the personal info of the person with the specified id.

        Parameters
        ----------
        speaker_id: str, required
            The id of the speaker.

        Returns
        -------
        personal_info: dict
            The personal info.
        """ ""
        if not speaker_id.startswith('#'):
            speaker_id = '#' + speaker_id
        actual_name = self.__id_map[speaker_id]
        speaker_info = self.__info_resolver.resolve(actual_name)
        if speaker_info is not None:
            return speaker_info
        # TODO: Build speaker info from name
        return SpeakerInfoProvider.EMPTY_SPEAKER

    def get_speaker_name(self, full_name: str) -> str:
        """Get the speaker name.

        Parameters
        ----------
        full_name: str, required
            The full name of the speaker as it appears in the transcription.

        Returns
        -------
        speaker_name: str
            The name of the speaker.
        """
        actual_name = self.__name_resolver.resolve_name(full_name)
        if actual_name is None:
            logging.error("Could not resolve name '%s'.", full_name)
            return full_name
        return actual_name
