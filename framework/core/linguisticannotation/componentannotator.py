"""Defines a class for annotating component files."""
from framework.core.linguisticannotation.linguisticannotator import LinguisticAnnotator
from framework.core.linguisticannotation.sentencebuilder import SentenceBuilder
from framework.core.xmlutils import XmlDataManipulator
from framework.core.xmlutils import XmlElements
from pathlib import Path
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

    def apply_annotation(self):
        """Apply linguistic annotations to the file."""
        logging.info("Annotating file {}.".format(self.__file_name))
        for seg in self.xml_root.iterdescendants(tag=XmlElements.seg):
            if (seg.text is not None) and (len(seg.text) > 0):
                self.__replace_segment_text(seg)

        self.save_changes(self.__annotated_file)

    def __replace_segment_text(self, segment):
        """Replace the text of the specified segment with the provided sentences.

        Parameters
        ----------
        segment : etree.Element, required
            The segment whose text is to be replaced.
        """
        doc = self.__annotator.annotate(segment.text)
        segment.text = None
        builder = SentenceBuilder(segment)
        for sentence in doc.sents:
            builder.add_sentence(sentence._.conll_pd, sentence.ents)

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
