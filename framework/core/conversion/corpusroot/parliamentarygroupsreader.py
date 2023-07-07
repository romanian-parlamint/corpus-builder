"""Defines a class for reading parliamentary groups from CSV files."""
from typing import List
from framework.core.conversion.namedtuples import ParliamentaryGroup
import pandas as pd
from pathlib import Path


class ParliamentaryGroupsReader:
    """Reads parliamentary groups from CSV files."""

    def read(
        self,
        data_directory: str,
        file_name_pattern: str = 'parliamentary-groups.csv'
    ) -> List[ParliamentaryGroup]:
        """Read parliamentary groups from the specified directory.

        Parameters
        ----------
        data_directory: str, required
            The path of the directory containing CSV files with parliamentary groups.
        file_name_pattern: str, optional
            The pattern of the file names containing parliamentary groups.

        Returns
        -------
        parliamentarty_groups: list of ParliamentaryGroup
            The list of unique parliamentary groups.
        """
        data_dir = Path(data_directory)
        parla_groups = set()
        for f in data_dir.glob(f'**/{file_name_pattern}'):
            df = pd.read_csv(str(f))
            for row in df.itertuples():
                grp = ParliamentaryGroup(row.Acronym, row.Name)
                parla_groups.add(grp)

        return list(sorted(parla_groups, key=lambda grp: grp.Acronym))
