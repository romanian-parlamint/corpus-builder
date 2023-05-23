"""Defines a class for applying linguistic annotation."""
from framework.core.linguisticannotation.constants import MODEL
from spacy_conll import init_parser
from typing import Tuple
from pandas import DataFrame
from spacy.tokens import Doc


class LinguisticAnnotator:
    """Applies linguistic annotation to provided text."""

    def __init__(self):
        """Create a new instance of the class."""
        self.__nlp_pipeline = init_parser(MODEL, 'spacy')

    def annotate(self, sentence: str) -> Doc:
        """Apply linguistic annotation to the provided sentence.

        Parameters
        ----------
        sentence: str, required
            The sentence to annotate.

        Returns
        -------
        doc: spacy.tokens.Doc
            The annotated document.
        """
        doc = self.__nlp_pipeline(sentence)
        return doc
