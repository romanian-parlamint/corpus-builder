"""Defines a class for annotating component files."""
from framework.core.constants import SAMPLE_TAG
from framework.core.constants import SAMPLE_TAG_ANA
from framework.core.linguisticannotation.linguisticannotator import LinguisticAnnotator
from framework.core.linguisticannotation.sentencebuilder import SentenceBuilder
from framework.core.xmlutils import TitleTypes
from framework.core.xmlutils import XmlAttributes
from framework.core.xmlutils import XmlDataManipulator
from framework.core.xmlutils import XmlElements
from lxml import etree
from pathlib import Path
from typing import List
import logging


class CorpusComponentAnnotator(XmlDataManipulator):
    """Applies linguistic annotation to a corpus component file."""

    def __init__(self, component_file: Path, annotator: LinguisticAnnotator):
        """Create a new instance of CorpusComponentAnnotator for the specified file.

        Parameters
        ----------
        component_file : pathlib.Path
            The path of the component file.
        annotator: LinguisticAnnotator, required
            The annotator.
        """
        file_name = str(component_file)
        XmlDataManipulator.__init__(self, file_name)
        self.__file_name = file_name
        self.__component_file = component_file
        self.__annotator = annotator
        self.__annotated_file = self.__build_output_file_name(
            self.__component_file)
        self.__update_component_file_id()
        self.__update_component_title()

    def apply_annotation(self) -> Path:
        """Apply linguistic annotations to the file.

        Returns
        -------
        annotated_file: Path
            The path of the annotated file.
        """
        logging.info("Annotating file {}.".format(self.__file_name))
        for seg in self.xml_root.iterdescendants(tag=XmlElements.seg):
            # If the segment does not have child elements (i.e. has only text)
            # then we replace the text with annotated sentences; otherwise
            # we need to replace the text, and the tail of each child element
            # with annotated sentences.
            if len(seg) == 0:
                self.__replace_simple_segment_text(seg)
            else:
                self.__replace_complex_segment_text(seg)

        self.save_changes(self.__annotated_file)
        return self.__annotated_file

    def __replace_complex_segment_text(self, segment: etree.Element):
        """Replace the text of a segment containing inner children elements with sentence elements.

        Parameters
        ----------
        segment : etree.Element, required
            The segment whose text is to be replaced.
        """
        builder = SentenceBuilder(segment)
        children = []
        if segment.text is not None:
            sentences = self.__build_sentence_elements(builder,
                                                       segment.text.strip())
            children.extend(sentences)
            segment.text = None
        # Iterate over children of the segment and annotate tail
        for child_elem in segment:
            children.append(child_elem)
            if not self.__has_tail(child_elem):
                continue

            sentences = self.__build_sentence_elements(builder,
                                                       child_elem.tail.strip())
            children.extend(sentences)
            child_elem.tail = None
            segment.remove(child_elem)

        for c in children:
            segment.append(c)

    def __has_tail(self, element: etree.Element) -> bool:
        """Check if the provided element has tail.

        Parameters
        ----------
        element: etree.Element, required
            The element to check.

        Returns
        -------
        has_tail: bool
            True if element has tail; False otherwise.
        """
        if element.tail is None:
            return False
        tail = element.tail.strip()
        return len(tail) > 0

    def __build_sentence_elements(self, builder: SentenceBuilder,
                                  text: str) -> List[etree.Element]:
        """Build sentence elements from the provided text.

        Parameters
        ----------
        builder: SentenceBuilder, required
            The builder of sentence elements.
        text: str, required
            The text from which to build sentence elements.

        Returns
        -------
        sentences: list of etree.Element
            The list of sentence elements built from the supplied text.
        """
        doc = self.__annotator.annotate(text)
        return [
            builder.build_sentence(sentence._.conll_pd, sentence.ents)
            for sentence in doc.sents
        ]

    def __replace_simple_segment_text(self, segment):
        """Replace the text of the specified segment with the provided sentences.

        Parameters
        ----------
        segment : etree.Element, required
            The segment whose text is to be replaced.
        """
        doc = self.__annotator.annotate(segment.text.strip())
        segment.text = None
        builder = SentenceBuilder(segment)
        for sentence in doc.sents:
            builder.add_sentence(sentence._.conll_pd, sentence.ents)

    def __update_component_title(self):
        """Update the title of the component."""
        title_stmt = next(
            self.xml_root.iterdescendants(tag=XmlElements.titleStmt))
        for title in title_stmt.iterdescendants(tag=XmlElements.title):
            title_type = title.get(XmlAttributes.element_type)
            if title_type == TitleTypes.Main:
                title.text = title.text.replace(SAMPLE_TAG, SAMPLE_TAG_ANA)

    def __update_component_file_id(self):
        """Update the id of the component file."""
        self.xml_root.set(XmlAttributes.xml_id, self.__annotated_file.stem)

    def __build_output_file_name(self, file_path: Path) -> Path:
        """Build the file name for the annotated component file.

        Parameters
        ----------
        file_path : pathlib.Path, required
            The path of the component file from which to infer output file name.

        Returns
        -------
        annotated_file : pathlib.Path
            The name of output file.
        """
        parent = file_path.parent
        stem = file_path.stem
        annotated_file = Path(parent, '{}.ana.xml'.format(stem))
        return annotated_file
