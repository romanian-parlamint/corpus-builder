"""Defines a class that builds the root file of the corpus."""
from babel.dates import format_date
from datetime import datetime
from framework.core.constants import SAMPLE_TAG
from framework.core.conversion.corpusroot.organizationslistreader import OrganizationsListReader
from framework.core.conversion.corpusroot.personlistmanipulator import PersonListManipulator
from framework.core.conversion.corpusroot.sessionspeakersreader import SessionSpeakersReader
from framework.core.conversion.namedtuples import PersonalInformation
from framework.core.conversion.namemapping.speakerinfoprovider import SpeakerInfoProvider
from framework.core.xmlstats import CorpusStatsWriter
from framework.core.xmlstats import SessionStatsReader
from framework.core.xmlutils import Languages
from framework.core.xmlutils import Resources
from framework.core.xmlutils import TitleTypes
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlDataManipulator
from framework.core.xmlutils import XmlElements
from lxml import etree
from pathlib import Path


class RootCorpusFileBuilder(XmlDataManipulator):
    """Builds the root file of the corpus."""

    def __init__(self,
                 file_path: str,
                 template_file: str,
                 speaker_info_provider: SpeakerInfoProvider,
                 person_list_manipulator: PersonListManipulator,
                 organizations_list_reader: OrganizationsListReader,
                 is_sample: bool,
                 append: bool = False):
        """Create a new instance of the class.

        Parameters
        ----------
        file_path: str, required
            The path of the corpus root file.
        template_file: str, required
            The path of the corpus root template file.
        speaker_info_provider: SpeakerInfoProvider, required
            An instance of SpeakerInfoProvider used for filling speaker info.
        person_list_manipulator: PersonListManipulator, required
            An instance of PersonListManipulator used for updating the list of speakers.
        organizations_list_reader: OrganizationsListReader, required
            An instance of OrganizationsListReader used for readin organization data.
        is_sample: bool, required
            A flag indicating whether the root file is part of a sample or full corpus.
        append: bool, optional
            A flag indicating whether to append to existing file or to start from scratch.
        """
        root_file = file_path if append else template_file
        XmlDataManipulator.__init__(self, root_file)
        self.__file_path = file_path
        self.__speaker_info_provider = speaker_info_provider
        self.__person_list = person_list_manipulator
        self.__org_list = organizations_list_reader
        self.__update_corpus_title(is_sample)

    def add_corpus_file(self, corpus_file: str):
        """Add the specified file to the corpus root file.

        Parameters
        ----------
        corpus_file: str, required
            The path of the file to add to the corpus.
        """
        self.__update_statistics(corpus_file)
        self.__update_speakers_list(corpus_file)
        self.__add_component_file(corpus_file)
        self.__sort_component_files()
        self.save_changes(self.__file_path)

    def __update_speakers_list(self, component_path: str):
        """Update the list of speakers with the speakers from the session transcript.

        Parameters
        ----------
        component_path: str, required
            The path of the corpus component file.
        """
        speaker_reader = SessionSpeakersReader(component_path)
        speaker_ids, gov_members = speaker_reader.get_speaker_ids()
        for speaker_id in speaker_ids:
            session_date = speaker_reader.session_date
            term = self.__org_list.get_legislative_term(session_date)
            pi = self.__speaker_info_provider.get_personal_info(speaker_id)
            profile = PersonalInformation(pi.first_name, pi.last_name, pi.sex,
                                          pi.profile_image)
            executive_term = None
            if speaker_id in gov_members:
                executive_term = self.__org_list.get_executive_term(
                    session_date)

            self.__person_list.add_or_update_person(speaker_id, profile, term,
                                                    executive_term)

    def __sort_component_files(self):
        """Sort component files by file name."""

        def get_component_path(element):
            if etree.QName(element).localname != "include":
                return ''
            return element.get("href")

        self.xml_root[:] = sorted(self.xml_root, key=get_component_path)

    def __add_component_file(self, component_path: str):
        """Add the component path to the `include` element.

        Parameters
        ----------
        component_path: str, required
            The path of the corpus component file.
        """
        etree.register_namespace("xsi", "http://www.w3.org/2001/XInclude")
        qname = etree.QName("http://www.w3.org/2001/XInclude", "include")
        include_element = etree.Element(qname)
        include_element.set("href", Path(component_path).name)
        self.xml_root.append(include_element)

    def __update_statistics(self, component_path: str):
        """Update the dates and values of `tagUsage` element with the values from the corpus component file.

        Parameters
        ----------
        component_path: str, required
            The path of the corpus component file.
        """
        provider = SessionStatsReader(component_path)
        writer = CorpusStatsWriter(self.xml_root, provider)
        writer.update_statistics()
        self.__update_corpus_span(provider.get_session_date())

    def __update_corpus_span(self, session_date: datetime.date):
        """Update the date span of the corpus with the given date.

        Parameters
        ----------
        session_date: datetime.date, required
            The date of the component file session.
        """
        date_element = self.__update_span_for_element(XmlElements.setting,
                                                      session_date)
        date_element = self.__update_span_for_element(XmlElements.bibl,
                                                      session_date)
        att_from = date_element.get(XmlAttributes.event_start)
        att_to = date_element.get(XmlAttributes.event_end)
        date_element.text = f'{att_from} - {att_to}'
        self.__update_span_in_corpus_title(att_from, att_to)

    def __update_span_in_corpus_title(self, start_date: str, end_date: str):
        """Update the corpus span in corpus title.

        Parameters
        ----------
        start_date: str, required
            The string representation of the start date from the corpus.
        end_date: str, required
            The string representation of the end date from the corpus.
        """
        title_stmt = next(
            self.xml_root.iterdescendants(tag=XmlElements.titleStmt))
        for title in title_stmt.iterdescendants(tag=XmlElements.title):
            title_type = title.get(XmlAttributes.type_)
            if title_type != TitleTypes.Subtitle:
                continue
            lang = title.get(XmlAttributes.lang)
            text = Resources.CorpusSubtitleEn if lang == Languages.English else Resources.CorpusSubtitleRo
            title.text = text.format(start_date, end_date)

    def __update_span_for_element(
            self, element_name: str,
            session_date: datetime.date) -> etree.Element:
        """Update the span of the corpus with the given date for the provided element.

        Parameters
        ----------
        element_name: str, required
            The name of the element for which to update corpus span.
        session_date: datetime.date, required
            The date of the component file session.

        Returns
        -------
        date_element: etree.Element
            The child ``date`` element that contains the corpus span for further processing.
        """
        parent = next(self.xml_root.iterdescendants(tag=element_name))
        date = next(parent.iterdescendants(tag=XmlElements.date))
        start_date, end_date = datetime.max, datetime.min

        start = date.get(XmlAttributes.event_start)
        if len(start) > 0:
            start_date = datetime.fromisoformat(start)

        end = date.get(XmlAttributes.event_end)
        if len(start) > 0:
            end_date = datetime.fromisoformat(end)

        if session_date < start_date.date():
            date.set(XmlAttributes.event_start,
                     format_date(session_date, "yyyy-MM-dd"))
        if session_date > end_date.date():
            date.set(XmlAttributes.event_end,
                     format_date(session_date, "yyyy-MM-dd"))
        return date

    def __update_corpus_title(self, is_sample: bool):
        """Update the corpus title to include sample tag.

        Parameters
        ----------
        is_sample: bool required
            The flag specifying whether the root file is part of a sample or not.
        """
        if not is_sample:
            return

        title_stmt = next(
            self.xml_root.iterdescendants(tag=XmlElements.titleStmt))
        for title in title_stmt.iterdescendants(tag=XmlElements.title):
            title_type = title.get(XmlAttributes.type_)
            if title_type != TitleTypes.Main:
                continue
            title.text = f'{title.text} {SAMPLE_TAG}'
