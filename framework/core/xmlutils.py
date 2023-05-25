"""Utilities for XML conversion."""
from lxml import etree
from typing import List
from pathlib import Path


class XmlElements:
    """Names of the XML elements to build or parse."""

    TEI = '{http://www.tei-c.org/ns/1.0}TEI'
    affiliation = '{http://www.tei-c.org/ns/1.0}affiliation'
    bibl = '{http://www.tei-c.org/ns/1.0}bibl'
    body = '{http://www.tei-c.org/ns/1.0}body'
    classDecl = '{http://www.tei-c.org/ns/1.0}classDecl'
    date = '{http://www.tei-c.org/ns/1.0}date'
    desc = '{http://www.tei-c.org/ns/1.0}desc'
    div = '{http://www.tei-c.org/ns/1.0}div'
    event = '{http://www.tei-c.org/ns/1.0}event'
    extent = '{http://www.tei-c.org/ns/1.0}extent'
    figure = '{http://www.tei-c.org/ns/1.0}figure'
    forename = '{http://www.tei-c.org/ns/1.0}forename'
    gap = '{http://www.tei-c.org/ns/1.0}gap'
    graphic = '{http://www.tei-c.org/ns/1.0}graphic'
    head = '{http://www.tei-c.org/ns/1.0}head'
    idno = '{http://www.tei-c.org/ns/1.0}idno'
    include = '{http://www.w3.org/2001/XInclude}include'
    kinesic = '{http://www.tei-c.org/ns/1.0}kinesic'
    label = '{http://www.tei-c.org/ns/1.0}label'
    link = '{http://www.tei-c.org/ns/1.0}link'
    linkGrp = '{http://www.tei-c.org/ns/1.0}linkGrp'
    listOrg = '{http://www.tei-c.org/ns/1.0}listOrg'
    listPerson = '{http://www.tei-c.org/ns/1.0}listPerson'
    measure = '{http://www.tei-c.org/ns/1.0}measure'
    meeting = '{http://www.tei-c.org/ns/1.0}meeting'
    name = '{http://www.tei-c.org/ns/1.0}name'
    note = '{http://www.tei-c.org/ns/1.0}note'
    org = '{http://www.tei-c.org/ns/1.0}org'
    orgName = '{http://www.tei-c.org/ns/1.0}orgName'
    pc = '{http://www.tei-c.org/ns/1.0}pc'
    persName = '{http://www.tei-c.org/ns/1.0}persName'
    person = '{http://www.tei-c.org/ns/1.0}person'
    s = '{http://www.tei-c.org/ns/1.0}s'
    seg = '{http://www.tei-c.org/ns/1.0}seg'
    setting = '{http://www.tei-c.org/ns/1.0}setting'
    sex = '{http://www.tei-c.org/ns/1.0}sex'
    surname = '{http://www.tei-c.org/ns/1.0}surname'
    tagUsage = '{http://www.tei-c.org/ns/1.0}tagUsage'
    text = '{http://www.tei-c.org/ns/1.0}text'
    title = '{http://www.tei-c.org/ns/1.0}title'
    titleStmt = '{http://www.tei-c.org/ns/1.0}titleStmt'
    u = '{http://www.tei-c.org/ns/1.0}u'
    w = '{http://www.tei-c.org/ns/1.0}w'


class XmlAttributes:
    """Constants used for names of XML attributes."""

    ana = 'ana'
    corresp = 'corresp'
    element_type = 'type'
    event_end = 'to'
    event_start = 'from'
    full = 'full'
    gi = 'gi'
    href = 'href'
    lang = '{http://www.w3.org/XML/1998/namespace}lang'
    lemma = 'lemma'
    meeting_n = 'n'
    msd = 'msd'
    occurs = 'occurs'
    pos = 'pos'
    quantity = 'quantity'
    ref = 'ref'
    role = 'role'
    role = 'role'
    targFunc = 'targFunc'
    target = 'target'
    type_ = 'type'
    unit = 'unit'
    url = 'url'
    value = 'value'
    when = 'when'
    who = 'who'
    xml_id = '{http://www.w3.org/XML/1998/namespace}id'


class Resources:
    """Resource strings."""

    SessionTitleRo = "Corpus parlamentar român ParlaMint-RO, ședința Camerei Deputaților din {}"
    SessionSubtitleRo = "Stenograma ședinței Camerei Deputaților din România din {}"
    SessionTitleEn = "Romanian parliamentary corpus ParlaMint-RO, Regular Session, Chamber of Deputies, {}"
    SessionSubtitleEn = "Minutes of the session of the Chamber of Deputies of Romania, {}"
    CorpusSubtitleRo = "Stenogramele ședințelor parlamentului României, {} - {}"
    CorpusSubtitleEn = "Meeting minutes of the Romanian parliament, {} - {}"
    Heading = "ROMÂNIA CAMERA DEPUTAȚILOR"
    SessionHeading = "Ședinta Camerei Deputaților din {}"
    ToC = "SUMAR"
    NumSpeechesRo = "{} discursuri"
    NumSpeechesEn = "{} speeches"
    NumWordsRo = "{} cuvinte"
    NumWordsEn = "{} words"
    RegularSession = "Sesiunea ordinară"
    ExtraordinarySession = "Sesiunea extraordinară"


class OrganizationRoles:
    """Constants for organization roles."""

    Parliament = "parliament"
    Government = "parliament"


class Languages:
    """Constants for languages."""

    Romanian = "ro"
    English = "en"


class Taxonomy:
    """Defines constants for taxonomy terms.""" ""

    Term = '#parla.term'
    Session = '#parla.session'
    Sitting = '#parla.sitting'


def load_xml(file_name):
    """Load the specified XML file.

    Parameters
    ----------
    file_name: str, required
        The name of the XML file.

    Returns
    -------
    xml_tree: etree.ElementTree
        The XML tree from the file.
    """
    parser = etree.XMLParser(remove_blank_text=True)
    xml_tree = etree.parse(file_name, parser)
    return xml_tree


def save_xml(xml: etree._ElementTree, file_name: str):
    """Save the provided XML tree to the specified file.

    Parameters
    ----------
    xml : etree.ElementRoot, required
        The XML tree to save to disk.
    file_name : str, required
        The file where to save the XML.
    """
    xml.write(file_name,
              pretty_print=True,
              encoding='utf-8',
              xml_declaration=True)


class XmlDataReader:
    """Provide basic abstractions for reading a XML file."""

    def __init__(self, xml_file: str):
        """Create a new instance of the class.

        Parameters
        ----------
        xml_file: str, required
            The path of the XML file.
        """
        self.__xml_file = xml_file
        self.__xml_tree = load_xml(xml_file)

    @property
    def xml_file(self) -> str:
        """Get the XML file."""
        return self.__xml_file

    @property
    def xml_tree(self):
        """Get the XML tree."""
        return self.__xml_tree

    @property
    def xml_root(self):
        """Get the root node of the XML tree."""
        return self.xml_tree.getroot()


class XmlDataManipulator(XmlDataReader):
    """Provide basic abstractions for manipulating a XML file."""

    def __init__(self, xml_file: str):
        """Create a new instance of the class.

        Parameters
        ----------
        xml_file: str, required
            The path of the XML file.
        """
        XmlDataReader.__init__(self, xml_file)

    def save_changes(self, output_file: str = None):
        """Save the changes made to the XML tree.

        Parameters
        ----------
        output_file: str, optional
            The file where to save the changes.
            If `None` then changes will be saved to the input file.
        """
        xml_file = output_file if output_file is not None else self.xml_file
        save_xml(self.xml_tree, xml_file)


class XsiIncludeElementsReader(XmlDataReader):
    """Read the include elements from the provided file."""

    def __init__(self, xml_file: str):
        """Create a new instance of the class.

        Parameters
        ----------
        xml_file: str, required
            The path of the XML file.
        """
        XmlDataReader.__init__(self, xml_file)

    def get_included_files(self, parent_element_name) -> List[Path]:
        """Read included files that are children of the specified element.

        Returns
        -------
        included_files: list of Path
            The list of file paths to include.
        """
        parent = None
        for elem in self.xml_root.iterdescendants(tag=parent_element_name):
            parent = elem
            break

        if parent is None:
            return []
        xml_file_path = Path(self.xml_file)
        files = []
        for elem in parent.iterdescendants(tag=XmlElements.include):
            included_file = elem.get(XmlAttributes.href)
            file_path = xml_file_path.parent / included_file
            files.append(file_path)
        return files
