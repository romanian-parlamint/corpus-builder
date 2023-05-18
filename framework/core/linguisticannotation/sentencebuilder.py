"""Defines class for building sentences."""
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlElements
from lxml import etree
from pandas import DataFrame
from spacy.tokens.span import Span
from typing import List
from typing import Tuple


class SentenceBuilder:
    """Builds the sentence elements."""

    def __init__(self, segment: etree.Element):
        """Create a new instance of the class.

        Parameters
        ----------
        segment: etree.Element, required
            The element to which to append sentences.
        """
        self.__segment = segment
        self.__sentence_index = 0
        self.__token_index = 0

    def add_sentence(self, sentence: DataFrame, named_entities: List[Span]):
        """Add the specified sentence to current segment.

        Parameters
        ----------
        sentence: pandas.DataFrame, required
            The sentence to add.
        named_entities: list of spacy Span, required
            The named entities of the sentence.
        """
        s = self.__create_sentence_element()
        for token in sentence.itertuples():
            self.__append_token(s, token)

    def __append_token(self, sentence: etree.Element, token: Tuple[any]):
        """Append the token to the sentence."""
        element_name = XmlElements.pc if token.UPOS == 'PUNCT' else XmlElements.w
        token_element = etree.SubElement(sentence, element_name)
        token_id = f'{sentence.get(XmlAttributes.xml_id)}.{token.Index}'
        token_element.set(XmlAttributes.xml_id, token_id)
        token_element.text = token.FORM
        if element_name == XmlElements.w:
            token_element.set(XmlAttributes.lemma, token.LEMMA)
        token_element.set(XmlAttributes.pos, token.XPOS)
        msd = f'UPosTag={token.UPOS}'
        if token.FEATS != '_':
            msd = msd + f'|{token.FEATS}'
        token_element.set(XmlAttributes.msd, msd)

    def __create_sentence_element(self) -> etree.Element:
        """Create a sentence element as a child element of the segment.

        Returns
        -------
        s: etree.Element
            The sentence element that was created.
        """
        segment_id = self.__segment.get(XmlAttributes.xml_id)
        sentence_id = f'{segment_id}.{self.__get_sentence_index()}'
        s = etree.SubElement(self.__segment, XmlElements.s)
        s.set(XmlAttributes.xml_id, sentence_id)
        return s

    def __get_sentence_index(self) -> int:
        """Return the sentence index and increments the counter."""
        self.__sentence_index += 1
        self.__token_index = 0
        return self.__sentence_index
