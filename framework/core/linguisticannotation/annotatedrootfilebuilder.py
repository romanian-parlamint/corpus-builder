"""Defines a class for building the annotated root file."""
from framework.core.xmlutils import XmlDataManipulator
from framework.core.xmlutils import XmlElements
from lxml import etree
from pathlib import Path
from typing import Iterable


class AnnotatedRootFileBuilder(XmlDataManipulator):
    """Builds the annotated root file."""

    def __init__(self, root_file: str, annotated_root_file: str,
                 taxonomy_files: Iterable[str]):
        """Create a new instance of the class.

        Parameters
        ----------
        root_file: str, required
            The path of the unannotated root corpus file.
        annotated_root_file: str, required
            The path of the annotated root corpus file.
        """
        XmlDataManipulator.__init__(self, root_file)
        self.__annotated_root_file = annotated_root_file
        self.__clean_include_tags()
        self.__add_taxonomy_files(taxonomy_files)

    def add_corpus_file(self, corpus_file: Path):
        """Add the specified component file to the root file.

        Parameters
        ----------
        corpus_file: Path, required
            The path of the corpus file.
        """
        self.__add_include_element(self.xml_root, corpus_file.name)
        self.save_changes(self.__annotated_root_file)

    def __add_taxonomy_files(self, taxonomy_files: Iterable[str]):
        """Add specified taxonomy files to `classDecl` element.

        Parameters
        ----------
        taxonomy_files: iterable of str, required
            The names of the taxonomy files.
        """
        class_decl = next(
            self.xml_root.iterdescendants(tag=XmlElements.classDecl))
        for taxonomy_file in taxonomy_files:
            self.__add_include_element(class_decl, taxonomy_file)

    def __add_include_element(self, parent: etree.Element, file_name: str):
        """Add an `include` element to the parent node with the provided file name.

        Parameters
        ----------
        parent: etree.Element, required
            The parent element to which to append the `include` element.
        file_name: str, required
            The name of the file referenced by the include element.
        """
        etree.register_namespace("xsi", "http://www.w3.org/2001/XInclude")
        qname = etree.QName("http://www.w3.org/2001/XInclude", "include")
        include_element = etree.Element(qname)
        include_element.set("href", file_name)
        parent.append(include_element)

    def __clean_include_tags(self):
        """Clean the include tags from the XML root."""
        for element in self.xml_root.findall(XmlElements.include):
            self.xml_root.remove(element)
