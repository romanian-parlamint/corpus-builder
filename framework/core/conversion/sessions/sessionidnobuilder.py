"""Defines a class for building the idno element."""
from framework.core.conversion.jsonutils import SessionTranscript
from framework.core.conversion.sessions.jsontranscripttoxmlconverter import JsonTranscriptToXmlConverter
from framework.core.conversion.xmlutils import XmlAttributes
from framework.core.conversion.xmlutils import XmlElements


class SessionIdNoBuilder(JsonTranscriptToXmlConverter):
    """Builds the idno element."""

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

    def build_session_idno(self):
        """Build the contents of the idno element."""
        for idno in self.xml_root.iterdescendants(tag=XmlElements.idno):
            if idno.get(XmlAttributes.element_type) == 'URI':
                idno.text = self.session_transcript.transcript_url

        self.save_changes()
