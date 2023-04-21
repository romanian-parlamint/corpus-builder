"""Defines a class for building the notes that contain start/end time of the session."""
from framework.core.conversion.sessions.debatesectionbuilder import DebateSectionBuilder
from framework.core.conversion.xmlutils import XmlAttributes
from framework.core.conversion.xmlutils import XmlElements
from lxml import etree


class SessionStartEndTimeBuilder(DebateSectionBuilder):
    """Builds the note elements containing the session start/end time."""

    def build_session_start_time(self):
        """Build session start time note."""
        start_time = self.session_transcript.start_mark
        if start_time is None:
            return

        note = etree.SubElement(self.debate_section, XmlElements.note)
        note.set(XmlAttributes.element_type, "time")
        note.text = start_time
        self.save_changes()

    def build_session_end_time(self):
        """Build session end time note."""
        end_time = self.session_transcript.end_mark
        if end_time is None:
            return

        note = etree.SubElement(self.debate_section, XmlElements.note)
        note.set(XmlAttributes.element_type, "time")
        note.text = end_time
        self.save_changes()
