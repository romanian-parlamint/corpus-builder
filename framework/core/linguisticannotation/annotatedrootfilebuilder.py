"""Defines a class for building the annotated root file."""
from framework.core.constants import SAMPLE_TAG
from framework.core.constants import SAMPLE_TAG_ANA
from framework.core.xmlutils import Languages
from framework.core.xmlutils import Resources
from framework.core.xmlutils import TitleTypes
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlDataManipulator
from framework.core.xmlutils import XmlElements
from lxml import etree
from pathlib import Path
from typing import Iterable

APP_INFO = """
      <appInfo>
         <application version="3.4.4" ident="app-spaCy">
            <label>spaCy</label>
            <desc xml:lang="en">
      <ref target="https://spacy.io/">spaCy</ref>: Industrial-Strength Natural Language Processing in Python.</desc>
         </application>
         <application version="3.4.0" ident="app-spaCy-ro-core-news-lg">
            <label>ro_core_news_lg</label>
            <desc xml:lang="en">
               <ref target="https://spacy.io/models/ro#ro_core_news_lg">ro_core_news_lg</ref> Romanian pipeline optimized for CPU. Components: tok2vec, tagger, parser, lemmatizer (trainable_lemmatizer), senter, ner, attribute_ruler.
            </desc>
         </application>
         <application version="3.4.0" ident="app-spacy-conll">
            <label>spaCy conll</label>
            <desc xml:lang="en">
               <ref target="https://github.com/BramVanroy/spacy_conll">spaCy conll</ref>: Pipeline component for spaCy (and other spaCy-wrapped parsers such as spacy-stanza and spacy-udpipe) that adds CoNLL-U properties to a Doc and its sentences and tokens. Can also be used as a command-line tool.
            </desc>
         </application>
      </appInfo>
"""


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
        self.__update_xml_id()
        self.__update_title()
        self.__clean_include_tags()
        self.__add_taxonomy_files(taxonomy_files)
        self.__add_app_info()

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
        self.__add_prefix_declarations()

    def __add_prefix_declarations(self):
        """Add prefix declarations after 'classDecl' element."""
        class_decl = next(
            self.xml_root.iterdescendants(tag=XmlElements.classDecl))
        list_prefix = etree.Element(XmlElements.listPrefixDef)
        class_decl.addnext(list_prefix)
        prefix_def = etree.SubElement(list_prefix,
                                      XmlElements.prefixDef,
                                      attrib={
                                          'ident': "ud-syn",
                                          'matchPattern': "(.+)",
                                          'replacementPattern': "#$1"
                                      })
        p = etree.SubElement(prefix_def,
                             XmlElements.p,
                             attrib={XmlAttributes.lang: Languages.Romanian})
        p.text = Resources.UdSynPrefixRo
        p = etree.SubElement(prefix_def,
                             XmlElements.p,
                             attrib={XmlAttributes.lang: Languages.English})
        p.text = Resources.UdSynPrefixEn

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

    def __update_xml_id(self):
        """Update the XML id of the root file."""
        self.xml_root.set(XmlAttributes.xml_id,
                          self.__annotated_root_file.stem)

    def __update_title(self):
        """Update the title of the corpus."""
        title_stmt = next(
            self.xml_root.iterdescendants(tag=XmlElements.titleStmt))
        for title in title_stmt.iterdescendants(tag=XmlElements.title):
            title_type = title.get(XmlAttributes.element_type)
            if title_type == TitleTypes.Main:
                title.text = title.text.replace(SAMPLE_TAG, SAMPLE_TAG_ANA)

    def __add_app_info(self):
        """Add the 'appInfo' element to the root file."""
        list_prefix = next(
            self.xml_root.iterdescendants(tag=XmlElements.listPrefixDef))
        app_info = etree.fromstring(APP_INFO)
        list_prefix.addnext(app_info)
