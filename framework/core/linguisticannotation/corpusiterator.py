"""Defines a class for iterating corpus files."""
from pathlib import Path
from typing import List


class CorpusIterator:
    """Defines methods for iterating over corpus files."""

    def __init__(self,
                 corpus_dir: str,
                 root_file: str = 'ParlaMint-RO.xml',
                 taxonomy_files: List[str] = [
                     'ParlaMint-taxonomy-NER.ana.xml',
                     'ParlaMint-taxonomy-parla.legislature.xml',
                     'ParlaMint-taxonomy-politicalOrientation.xml',
                     'ParlaMint-taxonomy-speaker_types.xml',
                     'ParlaMint-taxonomy-subcorpus.xml',
                     'ParlaMint-taxonomy-UD-SYN.ana.xml'
                 ]):
        """Create a new instance of CorpusIterator.

        Parameters
        ----------
        corpus_dir : str, required
            The path to the corpus directory.
        root_file : str, required
            The name of the root file in corpus.
        taxonomy_files: list of str, required
            The list of taxonomy files.
        """
        self.__corpus_dir = Path(corpus_dir)
        self.__corpus_root_file = Path(self.__corpus_dir, root_file)
        self.__taxonomy_files = taxonomy_files
        self.__annotated_corpus_root_file = self.__corpus_dir / f'{self.__corpus_root_file.stem}.ana.xml'

    @property
    def root_file(self):
        """Get the root file of the corpus.

        Returns
        -------
        root_file: pathlib.Path
            The path of the root file.
        """
        return self.__corpus_root_file

    @property
    def annotated_root_file(self):
        """Get the annotated root file of the corpus.

        Returns
        -------
        annotated_root_file: pathlib.Path
            The path of the annotated root file.
        """
        return self.__annotated_corpus_root_file

    def iter_corpus_files(self):
        """Iterate over corpus files.

        Returns
        -------
        file_generator: generator of pathlib.Path
            The generator that iterates corpus files one by one.
        """
        for file_path in self.__corpus_dir.glob("*.xml"):
            if file_path == self.root_file:
                continue
            if '.ana' in file_path.suffixes:
                continue
            if file_path.name in self.__taxonomy_files:
                continue
            yield file_path

    def iter_annotated_files(self):
        """Iterate over annotated corpus files.

        Returns
        -------
        file_generator: generator of pathlib.Path
            The generator that iterates annotated corpus files one by one.
        """
        for file_path in self.__corpus_dir.glob("*.ana.xml"):
            if file_path == self.annotated_root_file:
                continue
            yield file_path

    def get_component_file_name(self, file_path):
        """Get the name of the component file associated with the provided file.

        Parameters
        ----------
        file_path: pathlib.Path, required
            The path of the file for which to get the component file.

        Returns
        -------
        component_file: pathlib.Path
            The component file path.
        """
        stem = self._get_file_name_without_extensions(file_path)
        component_file = Path(file_path).with_stem(stem)
        component_file = component_file.with_suffix(".xml")
        return component_file

    def _get_file_name_without_extensions(self, file_path):
        """Get the file name by replacing all extensions with empty strings.

        Parameters
        ----------
        file_path: pathlib.Path, required
            The path of the file.

        Returns
        -------
        stem: str
            File name without extensions.
        """
        stem = file_path.stem
        for ext in file_path.suffixes:
            stem = stem.replace(ext, '')
        return stem
