"""Defines a class for building the node containing the chairmen of the session."""
from framework.core.conversion.sessions.debatesectionbuilder import DebateSectionBuilder
from framework.core.conversion.xmlutils import XmlAttributes
from framework.core.conversion.xmlutils import XmlElements
from lxml import etree


class SessionChairmenBuilder(DebateSectionBuilder):
    """Builds the node containing info about the chairmen of the session."""

    def build_session_chairmen(self):
        """Build the node containing session chairmen."""
        chairman = self.session_transcript.chairman
        if chairman is None:
            return

        note = etree.SubElement(self.debate_section, XmlElements.note)
        note.set(XmlAttributes.element_type, "narrative")
        note.text = chairman
        self.save_changes()
