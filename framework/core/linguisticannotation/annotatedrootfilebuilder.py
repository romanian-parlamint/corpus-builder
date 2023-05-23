"""Defines a class for building the annotated root file."""
from framework.core.xmlutils import XmlDataManipulator
from framework.core.xmlutils import XmlElements
from lxml import etree
from pathlib import Path


class AnnotatedRootFileBuilder(XmlDataManipulator):
    """Builds the annotated root file."""

    def __init__(self, root_file: str, annotated_root_file: str):
        """Create a new instance of the class.

        Parameters
        ----------
        root_file: str, required
            The path of the unannotated root corpus file.
        annotated_root_file: str, required
            The path of the annotated root corpus file.
        """
        XmlDataManipulator.__init__(self, root_file)
        self.__clean_include_tags()
        self.__annotated_root_file = annotated_root_file

    def add_corpus_file(self, corpus_file: Path):
        """Add the specified component file to the root file.

        Parameters
        ----------
        corpus_file: Path, required
            The path of the corpus file.
        """
        etree.register_namespace("xsi", "http://www.w3.org/2001/XInclude")
        qname = etree.QName("http://www.w3.org/2001/XInclude", "include")
        include_element = etree.Element(qname)
        include_element.set("href", corpus_file.name)
        self.xml_root.append(include_element)
        self.save_changes(self.__annotated_root_file)

    def __clean_include_tags(self):
        """Clean the include tags from the XML root."""
        for element in self.xml_root.iterdescendants(tag=XmlElements.include):
            element.getparent().remove(element)
