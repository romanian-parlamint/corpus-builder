"""Defines a class for building session title."""
from babel.dates import format_date
from framework.core.conversion.jsonutils import SessionTranscript
from framework.core.conversion.sessions.jsontranscripttoxmlconverter import JsonTranscriptToXmlConverter
from framework.core.xmlutils import Languages
from framework.core.xmlutils import Resources
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlElements


class SessionTitleBuilder(JsonTranscriptToXmlConverter):
    """Builds the session title."""

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

    def build_session_title(self, add_sample_tag: bool = False):
        """Build session title.

        Parameters
        ----------
        add_sample_tag: bool, optional
            Instructs the builder to add sample tag when true.
        """
        session_date = self.session_transcript.session_date
        ro_date = format_date(session_date, "d MMMM yyyy", locale="ro")
        en_date = format_date(session_date, "MMMM d yyyy", locale="en")

        for elem in self.xml_root.iterdescendants(tag=XmlElements.title):
            if elem.getparent().tag != XmlElements.titleStmt:
                continue

            title_type = elem.get(XmlAttributes.element_type)
            lang = elem.get(XmlAttributes.lang)
            if title_type == 'main' and lang == Languages.Romanian:
                elem.text = Resources.SessionTitleRo.format(ro_date)
                if add_sample_tag:
                    elem.text = elem.text + ' [ParlaMint SAMPLE]'

            if title_type == 'main' and lang == Languages.English:
                elem.text = Resources.SessionTitleEn.format(en_date)
                if add_sample_tag:
                    elem.text = elem.text + ' [ParlaMint SAMPLE]'

            if title_type == 'sub' and lang == Languages.Romanian:
                elem.text = Resources.SessionSubtitleRo.format(ro_date)

            if title_type == 'sub' and lang == Languages.English:
                elem.text = Resources.SessionSubtitleEn.format(en_date)

        self.save_changes()
