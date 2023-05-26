"""Defines a class for building the contents of the meeting elements.""" ""
from babel.dates import format_date
from datetime import datetime
from framework.core.conversion.jsonutils import SessionTranscript
from framework.core.conversion.namedtuples import LegislativeTerm
from framework.core.conversion.sessions.jsontranscripttoxmlconverter import JsonTranscriptToXmlConverter
from framework.core.xmlutils import Resources
from framework.core.xmlutils import Taxonomy
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlElements
from lxml import etree
from typing import List
from typing import Tuple
import logging


class MeetingElementContentsBuilder(JsonTranscriptToXmlConverter):
    """Builds the contents of the meeting elements."""

    def __init__(self, session_transcript: SessionTranscript,
                 legislative_terms: List[LegislativeTerm], xml_file: str):
        """Create a new instance of the class.

        Parameters
        ----------
        session_transcript: SessionTranscript, required
            The session transcript.
        legislative_terms: list of LegislativeTerm, required
            The list of legislative terms.
        xml_file: str, required
            The file containing session transcript in XML format.
        """
        JsonTranscriptToXmlConverter.__init__(self, session_transcript,
                                              xml_file)
        self.__terms = legislative_terms

    def build_meeting_info(self):
        """Build meeting element contents."""
        session_date = self.session_transcript.session_date

        for meeting in self.xml_root.iterdescendants(tag=XmlElements.meeting):
            meeting.set(XmlAttributes.corresp, "#RoParl")
            analysis_attr = meeting.get(XmlAttributes.ana)
            if Taxonomy.Term in analysis_attr:
                self.__set_term_info(meeting, session_date)
            if Taxonomy.Session in analysis_attr:
                self.__set_session_info(meeting, session_date)
            if Taxonomy.Sitting in analysis_attr:
                self.__set_sitting_info(meeting, session_date)

        self.save_changes()

    def __set_term_info(self, meeting: etree.Element, session_date: datetime):
        """Set the term information in the meeting element.

        Parameters
        ----------
        meeting: lxml:Element, required
            The meeting element.
        session_date: datetime, required
            The date of the session.
        """
        term = self.__get_term(session_date)
        if term is None:
            logging.error("Could not find legislative term for date %s.",
                          format_date(session_date, "yyyy-MM-dd"))
            parent = meeting.getparent()
            parent.remove(meeting)
        else:
            meeting.set(XmlAttributes.meeting_n, term.number)
            meeting.text = term.description

    def __get_term(self, session_date: datetime) -> LegislativeTerm:
        """Get the legislative term corresponding to the provided session date.

        Parameters
        ----------
        session_date: datetime, required
            The date of the session.
        """
        for term in self.__terms:
            end_date = datetime.max.date()
            if term.end_date is not None:
                end_date = term.end_date
            if term.start_date <= session_date <= end_date:
                return term
        return None

    def __set_session_info(self, meeting: etree.Element,
                           session_date: datetime):
        """Set the session information in the meeting element.

        Parameters
        ----------
        meeting: lxml:Element, required
            The meeting element.
        session_date: datetime, required
            The date of the session.
        """
        session_number, is_regular = self.__get_session_number(session_date)
        meeting.set(XmlAttributes.meeting_n, f'{session_number}')
        analysis_attr = meeting.get(XmlAttributes.ana)
        if is_regular:
            meeting.set(XmlAttributes.ana,
                        f'{analysis_attr} #parla.meeting.regular')
            meeting.text = f'{Resources.RegularSession} {session_number}'
        else:
            meeting.set(XmlAttributes.ana,
                        f'{analysis_attr} #parla.meeting.extraordinary')
            meeting.text = f'{Resources.ExtraordinarySession} {session_number}'

    def __get_session_number(
            self, session_date: datetime) -> Tuple[int | float, bool]:
        """Compute the session number based on the date.

        Parameters
        ----------
        session_date: datetime, required
            The date of the session.

        Returns
        -------
        (session_number,is_regular): tuple of (int or float, boolean)
            If the session date falls within the dates of a regular session,
            as specified in the parliamentary procedures (https://www.cdep.ro/pls/dic/site.page?id=319),
            the number of the session is returned as an int (either 1 or 2); otherwise a float is returned in the format
            of `<previous regular session number>.1`. If no previous regular session exists in the same year, returns 0.1.
        """
        if session_date.month < 2:
            # First extraordinary session of the year
            return 0.1, False
        if 2 <= session_date.month <= 6:
            # First regular session of the year
            return 1, True
        if 7 <= session_date.month <= 8:
            # Second extraordinary session of the year
            return 1.1, False
        if 9 <= session_date.month:
            return 2, True

    def __set_sitting_info(self, meeting: etree.Element,
                           session_date: datetime):
        """Set the sitting info in the meeting element.

        Parameters
        ----------
        meeting: lxml:Element, required
            The meeting element.
        session_date: datetime, required
            The date of the session.
        """
        meeting.set(XmlAttributes.meeting_n,
                    format_date(session_date, "yyyyMMdd"))
        meeting.text = format_date(session_date, "yyyy-MM-dd")
