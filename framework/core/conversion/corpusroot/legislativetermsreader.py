"""Defines a class for reading legislative terms."""

from datetime import date
from framework.core.conversion.namedtuples import LegislativeTerm
from framework.core.xmlutils import Languages
from framework.core.xmlutils import OrganizationRoles
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlElements
from lxml import etree
from typing import Generator
from typing import List
import logging


class LegislativeTermsReader:
    """Reads legislative terms from the root corpus file."""

    def __init__(self, xml_root: etree.Element):
        """Create a new instance of the class.

        Parameters
        ----------
        xml_root: etree.Element, required
            The root node of the corpus root file.
        """
        self.__xml_root = xml_root

    @property
    def __parliament(self):
        """Get the parliament organization.

        Returns
        -------
        parliament: etree.Element
            The element representing the parliament.
        """
        for org in self.__xml_root.iterdescendants(tag=XmlElements.org):
            if org.get(XmlAttributes.role) == OrganizationRoles.Parliament:
                return org
        return None

    def get_legislative_terms(self) -> List[LegislativeTerm]:
        """Get the legislative terms.

        Returns
        -------
        legislative_terms: list of LegislativeTerm
            The legislative terms.
        """
        if self.__parliament is None:
            logging.error("Could not find Parliament organization")
            return []

        return list(self.__load_legislative_terms())

    def __load_legislative_terms(
            self) -> Generator[LegislativeTerm, None, None]:
        """Load legislative terms from the XML.

        Returns
        -------
        terms: generator of LegislativeTerm
            The collection of terms.
        """
        for event in self.__parliament.iterdescendants(tag=XmlElements.event):
            term_id = event.get(XmlAttributes.xml_id)
            start_date = event.get(XmlAttributes.event_start)
            end_date = event.get(XmlAttributes.event_end)
            description = None
            for label in event.iterdescendants(tag=XmlElements.label):
                if label.get(XmlAttributes.lang) == Languages.Romanian:
                    description = label.text

            yield self.__build_legislative_term(term_id, start_date, end_date,
                                                description)

    def __build_legislative_term(self, term_id: str, start_date: str,
                                 end_date: str,
                                 description: str) -> LegislativeTerm:
        """Buils a legislative term from the provided data.

        Parameters
        ----------
        term_id: str, required
            The id of the term.
        start_date: str, required
            Start date of the term in ISO format.
        end_date: str, required
            End date of the term in ISO format.
        description: str, required
            The description of the term.
        """
        start_date = date.fromisoformat(start_date)
        end_date = None if end_date is None else date.fromisoformat(end_date)
        term_no = term_id.split('.')[-1]
        return LegislativeTerm(f'#{term_id}', term_no, start_date, end_date,
                               description)
