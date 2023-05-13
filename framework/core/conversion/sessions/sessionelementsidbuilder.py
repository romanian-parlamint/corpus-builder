"""Defines a class that builds the ids of the XML elements."""
from framework.core.xmlutils import XmlAttributes
from lxml import etree


class SessionElementsIdBuilder:
    """Builds the xml:id attribute for session elements.""" ""

    def __init__(self, xml_root: etree.Element):
        """Create a new instance of the class.

        Parameters
        ----------
        xml_root: etree.Element, required
            The root element of the session XML.
        """ ""
        self.__session_id = xml_root.get(XmlAttributes.xml_id)
        self.__utterance_id = 0
        self.__segment_id = 0

    def get_utterance_id(self) -> str:
        """Get the next id of an 'u' element.

        Returns
        -------
        utterance_id: str
            The id of the utterance element.
        """
        self.__utterance_id += 1
        self.__segment_id = 0
        return "{session}.u{utterance}".format(session=self.__session_id,
                                               utterance=self.__utterance_id)

    def get_segment_id(self) -> str:
        """Get the id of a 'seg' element.

        Returns
        -------
        segment_id: str
            The id of the segment element.
        """ ""
        self.__segment_id += 1
        return "{session}.u{utterance}.seg{segment}".format(
            session=self.__session_id,
            utterance=self.__utterance_id,
            segment=self.__segment_id)
