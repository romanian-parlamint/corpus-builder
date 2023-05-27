"""Defines the class that builds the session body.""" ""
from framework.core.conversion.jsonutils import BodySegment
from framework.core.conversion.jsonutils import SessionContentLine
from framework.core.conversion.jsonutils import SessionTranscript
from framework.core.conversion.jsonutils import Speaker
from framework.core.conversion.namemapping import SpeakerInfoProvider
from framework.core.conversion.sessions.debatesectionbuilder import DebateSectionBuilder
from framework.core.conversion.sessions.sessionelementsidbuilder import SessionElementsIdBuilder
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlElements
from lxml import etree
from typing import List
import re
from framework.core.constants import STR_TRANSLATIONS


class SessionBodyBuilder(DebateSectionBuilder):
    """Builds the nodes containing the session body."""

    def __init__(self, session_transcript: SessionTranscript,
                 speaker_info_provider: SpeakerInfoProvider, xml_file: str):
        """Create a new instance of the class.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        xml_file: str, required
            The file containing session transcript in XML format.
        speaker_info_provider: SpeakerInfoProvider, required
            An instance of SpeakerInfoProvider used for building speaker id.
        """
        super().__init__(session_transcript, xml_file)
        self.__element_id_builder = SessionElementsIdBuilder(self.xml_root)
        self.__speaker_info_provider = speaker_info_provider

    def build_session_body(self):
        """Build the session body."""
        session_segments = self.session_transcript.body
        if len(session_segments) == 0:
            return

        chairman = self.__get_speaker(session_segments, 0)
        chairman_name = self.__get_speaker_name(chairman)
        for idx, segment in enumerate(session_segments):
            if segment.is_empty:
                continue

            speaker = self.__get_speaker(session_segments, idx)
            speaker_name = self.__get_speaker_name(speaker)

            self.__build_speaker_note(speaker.announcement)
            utterance = self.__build_utterance(speaker_name, chairman_name)
            for content_line in segment.contents:
                if content_line.is_empty:
                    continue

                if len(content_line.annotations) == 0:
                    self.__build_simple_segment(utterance, content_line.text)
                else:
                    self.__build_complex_segment(utterance, content_line)
            if len(utterance) == 0:
                gap = etree.SubElement(utterance, XmlElements.gap,
                                       {"reason": "editorial"})
                desc = etree.SubElement(gap, XmlElements.desc)
                desc.text = "Lipsesc informații din cauza unei erori în modulul de descărcare date."

        self.save_changes()

    def __build_simple_segment(self, utterance: etree.Element, text: str):
        """Build a segment element with text contents.

        Parameters
        ----------
        utterance: etree.Element, required
            The parent utterance element.
        text: str, required
            The contents of the segment.
        """
        seg = etree.SubElement(utterance, XmlElements.seg)
        seg.set(XmlAttributes.xml_id,
                self.__element_id_builder.get_segment_id())
        seg.text = text.translate(STR_TRANSLATIONS)

    def __build_complex_segment(self, utterance: etree.Element,
                                content_line: SessionContentLine):
        """Build a segment element and add it to the parent utterance element.

        Parameters
        ----------
        utterance: etree.Element, required
            The parent utterance element.
        content_line: SessionContentLine, required
            The contents of the segment.
        """
        text = content_line.text
        seg = '<seg xml:id="{seg_id}">'
        for annotation in content_line.annotations:
            annotation = annotation.strip()
            first, *rest = text.split(annotation)
            replacement = self.__convert_annotation_to_element(annotation)
            seg = seg + "{} {} ".format(first, replacement)
            text = ''.join(rest)

        seg = seg + text + '</seg>'
        seg = seg.format(seg_id=self.__element_id_builder.get_segment_id())
        seg = re.sub(r'\s+', ' ', seg)
        seg = seg.translate(STR_TRANSLATIONS)

        utterance.append(etree.fromstring(seg))

    def __convert_annotation_to_element(self, annotation: str) -> str:
        """Convert the provided annotation to an XML string.

        Parameters
        ----------
        annotation: str, required
            The text of the annotation.

        Returns
        -------
        xml_string: str
            The XML string of the annotation being converted.
        """
        template = '<note type="editorial">{}</note>'
        text = annotation.lower()
        if 'vocif' in text:
            template = '<vocal type="shouting"><desc>{}</desc></vocal>'
        if 'rumoare' in text:
            template = '<vocal type="murmuring"><desc>{}</desc></vocal>'
        if 'râsete' in text:
            template = '<vocal type="laughter"><desc>{}</desc></vocal>'
        if 'aplauze' in text:
            template = '<vocal type="noise"><desc>{}</desc></vocal>'
        if 'gălăgie' in text:
            template = '<vocal type="noise"><desc>{}</desc></vocal>'
        return template.format(annotation)

    def __build_utterance(self, speaker_name: str, chairman_name: str):
        """Build an utterance element and add it to the debate section.

        Parameters
        ----------
        speaker_name: str, required
            The name of the speaker.
        chairman_name: str, required
            The name of the session chairman.

        Returns
        -------
        utterance: etree.Element
            The utterance element.
        """
        utterance = etree.SubElement(self.debate_section, XmlElements.u)
        speaker_type = "#chair" if speaker_name == chairman_name else "#regular"
        utterance.set(XmlAttributes.ana, speaker_type)
        speaker_id = self.__speaker_info_provider.get_speaker_id(speaker_name)
        utterance.set(XmlAttributes.who, speaker_id)
        utterance.set(XmlAttributes.xml_id,
                      self.__element_id_builder.get_utterance_id())
        return utterance

    def __build_speaker_note(self, text: str):
        """Build a speaker note element and add it to the debate section.

        Parameters
        ----------
        text: str, required
            The text of the note.
        """
        note = etree.SubElement(self.debate_section, XmlElements.note)
        note.set(XmlAttributes.element_type, "speaker")
        note.text = text

    def __get_speaker(self, session_segments: List[BodySegment],
                      segment_index: int) -> Speaker:
        """Get the speaker for the segment at the specified index.

        Parameters
        ----------
        session_segments: list of BodySegment, required
            The session segments.
        segment_index: int, required
            The index of the segment for which to determine the speaker.

        Returns
        -------
        speaker: Speaker
            The speaker associated with the current segment.
        """
        # Iterate backwards from the current index until the first speaker that is not None
        while (segment_index >= 0):
            segment = session_segments[segment_index]
            speaker = segment.speaker
            if (speaker is not None) and (not speaker.is_empty):
                return speaker
            segment_index = segment_index - 1

        raise ValueError("Could not determine speaker.")

    def __get_session_chairman(self,
                               session_segments: List[BodySegment]) -> Speaker:
        """Get the chairman of the session from session segments.

        Parameters
        ----------
        session_segments: list of BodySegment, required
            The session segments.

        Returns
        -------
        chairman_name: Speaker
            The session chairman.
        """
        # The chairman is the first speaker of the session
        for segment in session_segments:
            if segment.speaker is not None:
                return segment.speaker
        raise ValueError("Could not determine the chairman of the session.")

    def __get_speaker_name(self, speaker: Speaker) -> str:
        """Get the speaker name from the provided segment.

        Parameters
        ----------
        speaker: Speaker, required
            The speaker of the session segment.

        Returns
        -------
        speaker_name: str
            The name of the speaker if found; None otherwise.
        """
        if speaker is None:
            return None

        return self.__speaker_info_provider.get_speaker_name(speaker.full_name)
