"""Defines a class for building the session heading."""
from framework.core.conversion.sessions.debatesectionbuilder import DebateSectionBuilder
from framework.core.conversion.xmlutils import XmlAttributes
from framework.core.conversion.xmlutils import XmlElements
from lxml import etree


class SessionHeadingBuilder(DebateSectionBuilder):
    """Builds the session heading."""

    def build_session_heading(self):
        """Build the session heading."""
        session_title = self.session_transcript.session_title
        if session_title is None:
            return
        note = etree.SubElement(self.debate_section, XmlElements.note)
        note.set(XmlAttributes.element_type, "editorial")
        note.text = session_title
        self.save_changes()
