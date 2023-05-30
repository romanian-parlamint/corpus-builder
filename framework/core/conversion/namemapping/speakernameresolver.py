"""Defines a class for resolving speaker name."""
from framework.core.conversion.namedtuples import NameCorrection
from typing import Dict
from typing import Iterable


class SpeakerNameResolver:
    """Resolves the correct speaker name from the name written in trascripts."""

    def __init__(self, name_corrections: Iterable[NameCorrection]):
        """Create a new instance of the class.

        Parameters
        ----------
        name_corrections: iterable of NameCorrection
            The collection of name corrections.
        """
        self.__name_map = self.__build_name_map(name_corrections)

    def resolve_name(self, written_name: str) -> str:
        """Resolve the written name to the actual name.

        Parameters
        ----------
        written_name: str, required
            The name to resolve, in the form as it was wrtitten.

        Returns
        -------
        actual_name: str
            The actual name if name was found; None otherwise.
        """
        if written_name in self.__name_map:
            return self.__name_map[written_name]
        return None

    def __build_name_map(
            self,
            name_corrections: Iterable[NameCorrection]) -> Dict[str, str]:
        """Build the name map dictionary.

        Parameters
        ----------
        name_corrections: iterable of NameCorrection, required
            The collection of name corrections from which to build the name name.

        Returns
        -------
        name_map: dict of (str, str)
            The name map.
        """
        name_map = {}
        for correction in name_corrections:
            name_map[correction.written_name] = correction.actual_name
            name_map[correction.actual_name] = correction.actual_name
        return name_map
