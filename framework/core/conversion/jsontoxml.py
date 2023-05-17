"""Module responsible for conversion from JSON to  XML."""
from framework.core.conversion.jsonutils import SessionTranscript
from framework.core.conversion.namedtuples import LegislativeTerm
from framework.core.conversion.namemapping import SpeakerInfoProvider
from framework.core.conversion.sessions.meetingelementcontentsbuilder import MeetingElementContentsBuilder
from framework.core.conversion.sessions.sessionbodybuilder import SessionBodyBuilder
from framework.core.conversion.sessions.sessionchairmenbuilder import SessionChairmenBuilder
from framework.core.conversion.sessions.sessiondatebuilder import SessionDateBuilder
from framework.core.conversion.sessions.sessionheadingbuilder import SessionHeadingBuilder
from framework.core.conversion.sessions.sessionidbuilder import SessionIdBuilder
from framework.core.conversion.sessions.sessionidnobuilder import SessionIdNoBuilder
from framework.core.conversion.sessions.sessionstartendtimebuilder import SessionStartEndTimeBuilder
from framework.core.conversion.sessions.sessionsummarybuilder import SessionSummaryBuilder
from framework.core.conversion.sessions.sessiontitlebuilder import SessionTitleBuilder
from framework.core.xmlstats import SessionStatsCalculator
from framework.core.xmlstats import SessionStatsWriter
from framework.core.xmlutils import XmlElements
from typing import List
import logging
import spacy

nlp_pipeline = spacy.load('ro_core_news_lg')


class SessionTranscriptConverter:
    """Convert session transcript from JSON to XML."""

    def __init__(self, input_file: str, session_template: str,
                 speaker_info_provider: SpeakerInfoProvider,
                 legislative_terms: List[LegislativeTerm], output_file: str):
        """Create a new instance of the class.

        Parameters
        ----------
        input_file: str, required
            The path of the session transcript in JSON format.
        session_template: str, required
            The path of the XML file containing session template.
        speaker_info_provider: SpeakerInfoProvider, required
            The instance of SpeakerInfoProvider used to get speaker data.
        legislative_terms: list of LegislativeTerm, required
            The list of legislative terms.
        output_file: str, required
            The path of the output file.
        """
        self.__input_file = input_file
        self.__session_template = session_template
        self.__speaker_info_provider = speaker_info_provider
        self.__legislative_terms = legislative_terms
        self.__output_file = output_file

    def covert(self, is_sample: bool = False):
        """Convert session transcript to XML format.

        Parameters
        ----------
        is_sample: bool, optional
            Specifies if the current session is a sample or not.
        """
        logging.info("Converting from {} to {}.".format(
            self.__input_file, self.__output_file))
        session_transcript = SessionTranscript(self.__input_file)
        self.__build_session_id(session_transcript)
        self.__build_session_title(session_transcript, is_sample)
        self.__build_meeting_contents(session_transcript)
        self.__build_idno_contents(session_transcript)
        self.__build_date_contents(session_transcript)
        self.__build_session_summary(session_transcript)
        self.__build_session_heading(session_transcript)
        self.__build_session_start_time(session_transcript)
        self.__build_session_chairmen(session_transcript)
        self.__build_session_body(session_transcript)
        self.__build_session_end_time(session_transcript)
        self.__update_session_stats(self.__output_file)

    def __update_session_stats(self, output_file: str):
        """Update the nodes containing session statistics.

        Parameters
        ----------
        output_file: str, required
            The path of the output XML file.
        """
        stats_provider = SessionStatsCalculator(output_file,
                                                nlp_pipeline.tokenizer)
        name_map = {
            "text": XmlElements.text,
            "body": XmlElements.body,
            "div": XmlElements.div,
            "head": XmlElements.head,
            "note": XmlElements.note,
            "u": XmlElements.u,
            "seg": XmlElements.seg,
            "kinesic": XmlElements.kinesic,
            "desc": XmlElements.desc,
            "gap": XmlElements.gap
        }
        aggregator = SessionStatsWriter(output_file, stats_provider, name_map)
        aggregator.update_statistics()

    def __build_session_body(self, session_transcript: SessionTranscript):
        """Build the session body.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        """
        builder = SessionBodyBuilder(session_transcript,
                                     self.__speaker_info_provider,
                                     self.__output_file)
        builder.build_session_body()

    def __build_session_chairmen(self, session_transcript: SessionTranscript):
        """Build the node containing the information about the session chairmen.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        """
        builder = SessionChairmenBuilder(session_transcript,
                                         self.__output_file)
        builder.build_session_chairmen()

    def __build_session_end_time(self, session_transcript: SessionTranscript):
        """Build the node containing the end time of the session.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        """
        builder = SessionStartEndTimeBuilder(session_transcript,
                                             self.__output_file)
        builder.build_session_end_time()

    def __build_session_start_time(self,
                                   session_transcript: SessionTranscript):
        """Build the node containing end time of the session.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        """
        builder = SessionStartEndTimeBuilder(session_transcript,
                                             self.__output_file)
        builder.build_session_start_time()

    def __build_session_heading(self, session_transcript: SessionTranscript):
        """Build the session heading.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        """
        builder = SessionHeadingBuilder(session_transcript, self.__output_file)
        builder.build_session_heading()

    def __build_session_summary(self, session_transcript: SessionTranscript):
        """Build the session summary.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        """
        builder = SessionSummaryBuilder(session_transcript, self.__output_file)
        builder.build_summary()

    def __build_date_contents(self, session_transcript: SessionTranscript):
        """Build contents of date elements.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        """
        builder = SessionDateBuilder(session_transcript, self.__output_file)
        builder.build_date_contents()

    def __build_idno_contents(self, session_transcript: SessionTranscript):
        """Build idno element.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        """
        builder = SessionIdNoBuilder(session_transcript, self.__output_file)
        builder.build_session_idno()

    def __build_meeting_contents(self, session_transcript: SessionTranscript):
        """Build meeting element.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        """
        builder = MeetingElementContentsBuilder(session_transcript,
                                                self.__legislative_terms,
                                                self.__output_file)
        builder.build_meeting_info()

    def __build_session_title(self, session_transcript: SessionTranscript,
                              is_sample: bool):
        """Build session title.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        is_sample: bool, required
            Determines whether to build the title of a sample session or not.
        """
        builder = SessionTitleBuilder(session_transcript, self.__output_file)
        builder.build_session_title(add_sample_tag=is_sample)

    def __build_session_id(self, session_transcript: SessionTranscript):
        """Build session id.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        """
        session_id_builder = SessionIdBuilder(self.__session_template,
                                              session_transcript,
                                              self.__output_file)
        session_id_builder.build_session_id()
