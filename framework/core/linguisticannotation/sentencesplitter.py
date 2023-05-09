"""Defines a class for splitting text into sentences."""
import spacy
from typing import List
from framework.core.linguisticannotation.constants import MODEL

SENTENCE_SPLITTING_PIPES = ['tok2vec', 'parser', 'senter']


class SentenceSplitter:
    """Splits text into sentences."""

    def __init__(self):
        """Create a new instance of the class."""
        self.__nlp_pipeline = spacy.load(MODEL)

    def split(self, text: str) -> List[str]:
        """Split the provided text into sentences.

        Parameters
        ----------
        text: str, required
            The text to split into sentences.

        Returns
        -------
        sentences: list of str
            The sentences of the text.
        """
        with self.__nlp_pipeline.select_pipes(enable=SENTENCE_SPLITTING_PIPES):
            doc = self.__nlp_pipeline(text)
        return [sentence.text.strip() for sentence in doc.sents]
