"""Defines a class for building the contents of date elements."""
from babel.dates import format_date
from framework.core.conversion.jsonutils import SessionTranscript
from framework.core.conversion.sessions.jsontranscripttoxmlconverter import JsonTranscriptToXmlConverter
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlElements


class SessionDateBuilder(JsonTranscriptToXmlConverter):
    """Builds the contents of date elements."""

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

    def build_date_contents(self):
        """Build the content of date elements."""
        session_date = self.session_transcript.session_date
        for date in self.xml_root.iterdescendants(tag=XmlElements.date):
            parent_tag = date.getparent().tag
            if parent_tag == XmlElements.setting or parent_tag == XmlElements.bibl:
                date.set(XmlAttributes.when,
                         format_date(session_date, "yyyy-MM-dd"))
                date.text = format_date(session_date, "dd.MM.yyyy")

        self.save_changes()
