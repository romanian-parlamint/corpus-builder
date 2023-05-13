"""Defines a class for building session summary."""
from babel.dates import format_date
from framework.core.conversion.sessions.debatesectionbuilder import DebateSectionBuilder
from framework.core.xmlutils import Resources
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlElements
from lxml import etree


class SessionSummaryBuilder(DebateSectionBuilder):
    """Builds the session summary."""

    def build_summary(self):
        """Build the summary of the session."""
        self.__build_summary_heading()

        if len(self.session_transcript.summary) > 0:
            self.__build_table_of_contents()

        self.save_changes()

    def __build_table_of_contents(self):
        """Build the table of contents using summary elements."""
        self.__build_note("editorial", Resources.ToC)

        for summary_line in self.session_transcript.summary:
            for content in summary_line.contents:
                text = content.text
                if isinstance(text, str):
                    self.__build_note("summary", text)
                else:
                    for line in text:
                        self.__build_note("summary", line)

    def __build_note(self, note_type: str, text: str):
        """Build a child note element.

        Parameters
        ----------
        note_type: str, required
            The type of the note.
        text: str, required
            The text of the note.
        """
        note = etree.SubElement(self.debate_section, XmlElements.note)
        note.set(XmlAttributes.element_type, note_type)
        note.text = text

    def __build_summary_heading(self):
        """Build the heading nodes of the summary."""
        head = etree.SubElement(self.debate_section, XmlElements.head)
        head.text = Resources.Heading

        session_head = etree.SubElement(self.debate_section, XmlElements.head)
        session_head.set(XmlAttributes.element_type, "session")
        session_date = self.session_transcript.session_date
        session_date = format_date(session_date, "d MMMM yyyy")
        session_head.text = Resources.SessionHeading.format(session_date)
