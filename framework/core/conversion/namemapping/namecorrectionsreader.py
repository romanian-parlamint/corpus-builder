"""Defines class for reading name corrections."""
from framework.core.conversion.namedtuples import NameCorrection
import pandas as pd
from typing import List


class NameCorrectionsReader:
    """Reads name corrections from file."""

    def read(self, file_path: str) -> List[NameCorrection]:
        """Read name corrections from provided file.

        Parameters
        ----------
        file_path: str, required
            The path of the file containing name corrections.

        Returns
        -------
        corrections: list of NameCorrection
            The name corrections from the file.
        """
        df = pd.read_csv(file_path)
        return [
            NameCorrection(row.name, row.correct_name)
            for row in df.itertuples()
        ]
