"""Defines a class for building the debate section."""
from framework.core.conversion.jsonutils import SessionTranscript
from framework.core.conversion.sessions.jsontranscripttoxmlconverter import JsonTranscriptToXmlConverter
from framework.core.conversion.xmlutils import XmlAttributes
from framework.core.conversion.xmlutils import XmlElements
from lxml import etree


class DebateSectionBuilder(JsonTranscriptToXmlConverter):
    """A builder that works on the debate section."""

    def __init__(self, session_transcript: SessionTranscript, xml_file: str):
        """Create a new instance of the class.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        xml_file: str, required
            The file containing session transcript in XML format.
        """
        JsonTranscriptToXmlConverter.__init__(self, session_transcript,
                                              xml_file)
        self.__debate_section = None

    @property
    def debate_section(self) -> etree.Element:
        """Get the debate section of the XML.

        Returns
        -------
        debate_section, Element
            The debate section element.
        """
        if self.__debate_section is not None:
            return self.__debate_section

        for div in self.xml_root.iterdescendants(XmlElements.div):
            if div.get(XmlAttributes.element_type) == "debateSection":
                self.__debate_section = div
                return self.__debate_section
