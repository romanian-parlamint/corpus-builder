"""Defines a class for reading profile info of MPs."""
from ast import literal_eval
from framework.core.conversion.namemapping.speakerinfo import SpeakerInfo
from typing import Iterable
from typing import List
import logging
import pandas as pd


class SpeakerInfoReader:
    """Reads the profile info of speakers."""

    def __init__(self):
        """Create a new instance of the class."""
        self.__name_translations = str.maketrans({'Ş': 'Ș', 'ş': 'ș'})

    def read(self, file_path: str) -> List[SpeakerInfo]:
        """Read the profile info from the provided file.

        Parameters
        ----------
        file_path: str, required
            The path of the CSV file containing profile  info.

        Returns
        -------
        speaker_info: list of SpeakerInfo
            The profile info of speaker.
        """
        logging.info("Reading speaker info from %s.", file_path)
        names = set()
        personal_info = []
        df = pd.read_csv(file_path,
                         converters={
                             'first_name': literal_eval,
                             'last_name': literal_eval
                         })

        for row in df.itertuples():
            if row.full_name in names:
                logging.info("Name '%s' already read; skipping.",
                             row.full_name)
                continue
            profile_image = None if self.__is_empty(
                row.profile_image) else row.profile_image
            item = SpeakerInfo(self.__cleanup_name(row.first_name),
                               self.__cleanup_name(row.last_name),
                               sex=row.sex,
                               profile_image=profile_image)
            personal_info.append(item)
            names.add(row.full_name)
        return personal_info

    def __cleanup_name(self, name_parts: Iterable[str]) -> List[str]:
        """Cleanup the name.

        Parameters
        ----------
        name_parts: iterable of str, required
            The parts that constitute the name.

        Returns
        -------
        name: list of str
            The cleaned name after removing redundant data.
        """
        return [
            part.translate(self.__name_translations) for part in name_parts
            if self.__is_valid_name_part(part)
        ]

    def __is_valid_name_part(self, name_part: str) -> bool:
        """Check if provided name part is valid.

        Parameters
        ----------
        name_part: str, required
            The part of the name to check.

        Returns
        -------
        is_valid: bool
            True if the name part is valid; False otherwise.
        """
        if name_part is None or len(name_part) == 0:
            return False
        name_part = name_part.strip()
        if len(name_part) == 0:
            return False
        if name_part in ['-']:
            return False
        return True

    def __is_empty(self, value: str) -> bool:
        """Check if the provided value is empty.

        Parameters
        ----------
        value: str, required
            The value to check.

        Returns
        -------
        is_empty: bool
            True if value is empty; False otherwise.
        """
        return pd.isnull(value) or pd.isna(value) or len(value) == 0
