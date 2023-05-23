"""Defines class for building sentences."""
from framework.core.linguisticannotation.constants import NE_MAP
from framework.core.linguisticannotation.linkgroupbuilder import LinkGroupBuilder
from framework.core.linguisticannotation.namedentityfinder import NamedEntityFinder
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlElements
from lxml import etree
from pandas import DataFrame
from spacy.tokens.span import Span
from typing import Dict
from typing import List
import logging


class SentenceBuilder:
    """Builds the sentence elements."""

    def __init__(self,
                 segment: etree.Element,
                 named_entity_map: Dict[str, str] = NE_MAP):
        """Create a new instance of the class.

        Parameters
        ----------
        segment: etree.Element, required
            The element to which to append sentences.
        named_entity_map: dict of (str, str), optional
            The dictionary mapping named entity labels to the attribute values of 'name' element.
        """
        self.__segment = segment
        self.__ne_map = named_entity_map
        self.__sentence_index = 0
        self.__token_ids = set()

    def add_sentence(self, sentence: DataFrame, named_entities: List[Span]):
        """Add the specified sentence to current segment.

        Parameters
        ----------
        sentence: pandas.DataFrame, required
            The sentence to add.
        named_entities: list of spacy Span, required
            The named entities of the sentence.
        """
        self.__token_ids.clear()
        ne_finder = NamedEntityFinder(named_entities)
        s = self.__create_sentence_element()
        named_entity, name_element = None, None
        for token in sentence.itertuples():
            # Check if the current token is part of a named  entity (NE)
            named_entity = ne_finder.search_named_entity(token)
            # If token is not part of a NE, append it to the sentence element
            # and continue to the next token
            if named_entity is None:
                self.__append_token(s, s.get(XmlAttributes.xml_id), token)
                # Reset the reference to parent 'name' element since the current
                # token is not part of a NE.
                name_element = None
                continue
            # Here, the token is part of a NE, and we need to add it to a 'name' element.
            # First, we make sure that the 'name' element exists; if not we create one.
            if name_element is None:
                name_element = self.__build_name_element(
                    s, named_entity.label_)
            # Append the token to the 'name' element and continue to next token
            self.__append_token(name_element, s.get(XmlAttributes.xml_id),
                                token)

        link_builder = LinkGroupBuilder(s)
        link_builder.build_from(sentence)

    def __build_name_element(self, sentence: etree.Element,
                             named_entity_type: str) -> etree.Element:
        """Build the 'name' element with the provided named entity type.

        Parameters
        ----------
        sentence: etree.Element, required
            The parent sentence element to which to add name element.
        named_entity_type: str, required
            The type of the named entity.

        Returns
        -------
        name_elem: etree.Element,
            The name element.
        """
        name_elem = etree.SubElement(sentence, XmlElements.name)
        name_type = "MISC"
        if named_entity_type in self.__ne_map:
            name_type = self.__ne_map[named_entity_type]
        name_elem.set(XmlAttributes.type_, name_type)
        return name_elem

    def __append_token(self, parent: etree.Element, id_prefix: str,
                       token: any):
        """Append the token to the parent element.

        Parameters
        ----------
        parent: etree.Element, required
            The parent to which to append the token.
        id_prefix: str, required
            The prefix of the id attribute of the new element.
        token: a named tuple containing CoNLL-U properties, required
            The token to append.
        """
        element_name = XmlElements.pc if token.UPOS == 'PUNCT' else XmlElements.w

        token_element = etree.SubElement(parent, element_name)
        token_id = f'{id_prefix}.{token.ID}'
        if token_id in self.__token_ids:
            logging.error("Duplicate token id %s.", token_id)
        else:
            self.__token_ids.add(token_id)

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
        return self.__sentence_index
