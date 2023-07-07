"""Defines a class for reading coalition/opposition info from CSV files."""
from framework.core.conversion.namedtuples import CoalitionOppositionRelation
from pathlib import Path
from typing import List
import pandas as pd


class CoalitionOppositionRelationReader:
    """Reads the coalition/opposition info from CSV files."""

    def read(
        self,
        data_directory: str,
        file_name_pattern: str = 'coalition-opposition.csv'
    ) -> List[CoalitionOppositionRelation]:
        """Read coalition/opposition relations from CSV files from the specified directory.

        Parameters
        ----------
        data_directory: str, required
            The path of the directory containing CSV files with coalition/opposition relations.
        file_name_pattern: str, optional
            The pattern of the file names containing coalition/opposition relations.

        Returns
        -------
        relations: list of CoalitionOppositionRelation
            The list of coalition/opposition relations.
        """
        data_dir = Path(data_directory)
        relations = []
        for f in data_dir.glob(f'**/{file_name_pattern}'):
            df = pd.read_csv(str(f))
            for row in df.itertuples():
                coalition = self.__build_list(row.coalition)
                opposition = self.__build_list(row.opposition)
                relation = CoalitionOppositionRelation(row.start_date,
                                                       row.end_date, coalition,
                                                       opposition)
                relations.append(relation)
        return relations

    def __build_list(self, data: str) -> List[str]:
        """Split the data string into a list of values.

        Parameters
        ----------
        data: str, required
            The string to build the list from.

        Returns
        -------
        items: list of str
            The list of items built by splitting the data string.
        """
        return [item.strip() for item in data.split(sep=',')]
