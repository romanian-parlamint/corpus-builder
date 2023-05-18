"""Defines the class for building `linkGrp` elements."""
from lxml import etree
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlElements
from pandas import DataFrame


class LinkGroupBuilder:
    """Builds the `linkGrp` element of a sentence."""

    def __init__(self, sentence_element: etree.Element):
        """Create a new instance of LinkGroupBuilder for the specified sentence.

        Parameters
        ----------
        sentence_element: etree.Element, required
            The sentence element to which to add the link group.
        """
        self.__sentence_element = sentence_element

    def build_from(self, conllu_sentence: DataFrame):
        """Build the `linkGrp` element from the provided sentence as a CoNLL-U data frame.

        Parameters
        ----------
        conllu_sentence: DataFrame, required
            The sentence in CoNLL-U format.
        """
        linkGrp = self.__build_link_group_element()
        sentence_id = self.__sentence_element.get(XmlAttributes.xml_id)
        for token in conllu_sentence.itertuples():
            link = etree.SubElement(linkGrp, XmlElements.link)
            if token.DEPREL == 'ROOT':
                link.set(XmlAttributes.ana, f'ud-syn:{token.DEPREL.lower()}')
                link.set(XmlAttributes.target,
                         f'#{sentence_id} #{sentence_id}.{token.ID}')
            else:
                link.set(XmlAttributes.ana, f'ud-syn:{token.DEPREL}')
                link.set(
                    XmlAttributes.target,
                    f'#{sentence_id}.{token.HEAD} #{sentence_id}.{token.ID}')

    def __build_link_group_element(self):
        """Add the `linkGrp` element to the `s` element.

        Returns
        -------
        link_group: etree.Element
            The newly created `linkGrp` element.
        """
        link_group = etree.SubElement(self.__sentence_element,
                                      XmlElements.linkGrp)
        link_group.set(XmlAttributes.targFunc, "head argument")
        link_group.set(XmlAttributes.type_, "UD-SYN")
        return link_group
