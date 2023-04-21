"""Defines a class for building the contents of the meeting elements.""" ""
from babel.dates import format_date
from framework.core.conversion.jsonutils import SessionTranscript
from framework.core.conversion.sessions.jsontranscripttoxmlconverter import JsonTranscriptToXmlConverter
from framework.core.conversion.xmlutils import XmlAttributes
from framework.core.conversion.xmlutils import XmlElements


class MeetingElementContentsBuilder(JsonTranscriptToXmlConverter):
    """Builds the contents of the meeting elements."""

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

    def build_meeting_info(self):
        """Build meeting element contents."""
        session_date = self.session_transcript.session_date
        meeting_n = format_date(session_date, "yyyyMMdd")

        for meeting in self.xml_root.iterdescendants(tag=XmlElements.meeting):
            meeting.set(XmlAttributes.meeting_n, meeting_n)
            meeting.set(XmlAttributes.corresp, "#RoParl")

        self.save_changes()
