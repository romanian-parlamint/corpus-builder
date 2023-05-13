"""Defines a class for converting JSON transcript to XML."""
from framework.core.conversion.jsonutils import SessionTranscript
from framework.core.xmlutils import XmlDataManipulator


class JsonTranscriptToXmlConverter(XmlDataManipulator):
    """Base class for converting JSON transcript to XML.""" ""

    def __init__(self, session_transcript: SessionTranscript, xml_file: str):
        """Create a new instance of the class.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        xml_file: str, required
            The file containing session transcript in XML format.
        """
        XmlDataManipulator.__init__(self, xml_file)
        self.__transcript = session_transcript

    @property
    def session_transcript(self) -> SessionTranscript:
        """Get the session transcript.""" ""
        return self.__transcript
