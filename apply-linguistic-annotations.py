#!/usr/bin/env python
"""Perform linguistic annotation on the corpus."""
from argparse import ArgumentParser
from argparse import Namespace
from framework.core.linguisticannotation.annotatedrootfilebuilder import AnnotatedRootFileBuilder
from framework.core.linguisticannotation.componentannotator import CorpusComponentAnnotator
from framework.core.linguisticannotation.corpusiterator import CorpusIterator
from framework.core.linguisticannotation.linguisticannotator import LinguisticAnnotator
from framework.core.xmlstats import XmlTagCountWriter
from framework.core.xmlstats import XmlTagCounter
from framework.core.xmlutils import XmlElements
from framework.core.xmlutils import XsiIncludeElementsReader
from framework.utils.loggingutils import configure_logging
from typing import List
from pathlib import Path


def copy_taxonomy_files(taxonomy_files: List[str],
                        corpus_directory: str) -> List[Path]:
    """Copy taxonomy files to corpus directory.

    Parameters
    ----------
    taxonomy_files: list of str, required
        The list of taxonomy file paths to copy to corpus directory.
    corpus_directory: str, required
        The path of the corpus directory.

    Returns
    -------
    taxonomy_files: list of Path
        The paths of the taxonomy files within corpus directory.
    """
    results = []
    corpus_dir = Path(corpus_directory)
    for f in taxonomy_files:
        source_file = Path(f)
        destination_file = corpus_dir / source_file.name
        destination_file.write_text(source_file.read_text())
        results.append(destination_file)
    return results


def main(corpus_dir: str, root_file: str, taxonomy_files: List[str]):
    """Entry point of the module.

    Parameters
    ----------
    corpus_dir: str, required
        The directory containing XML transcript files.
    """
    root_file_path = Path(corpus_dir) / root_file
    common_taxonomies = XsiIncludeElementsReader(
        root_file_path).get_included_files(XmlElements.classDecl)
    annotation_taxonomies = copy_taxonomy_files(taxonomy_files, corpus_dir)
    iterator = CorpusIterator(
        corpus_dir,
        root_file=root_file,
        taxonomy_files=[
            t.name for t in common_taxonomies + annotation_taxonomies
        ])
    linguistic_annotator = LinguisticAnnotator()
    tag_map = {
        "body": XmlElements.body,
        "desc": XmlElements.desc,
        "div": XmlElements.div,
        "gap": XmlElements.gap,
        "head": XmlElements.head,
        "kinesic": XmlElements.kinesic,
        "link": XmlElements.link,
        "linkGrp": XmlElements.linkGrp,
        "name": XmlElements.name,
        "note": XmlElements.note,
        "pc": XmlElements.pc,
        "s": XmlElements.s,
        "seg": XmlElements.seg,
        "text": XmlElements.text,
        "u": XmlElements.u,
        "w": XmlElements.w,
    }
    root_file_builder = AnnotatedRootFileBuilder(
        iterator.root_file, iterator.annotated_root_file,
        [f.name for f in annotation_taxonomies])
    for component_file in iterator.iter_corpus_files():
        annotator = CorpusComponentAnnotator(component_file,
                                             linguistic_annotator)
        annotated_component_file = annotator.apply_annotation()
        counter = XmlTagCounter(annotated_component_file)
        count_writer = XmlTagCountWriter(annotated_component_file, tag_map)
        count_writer.update_tage_usage(counter.get_tag_counts())
        count_writer.save_changes()
        root_file_builder.add_corpus_file(annotated_component_file)


def parse_arguments() -> Namespace:
    """Parse command-line arguments.

    Returns
    -------
    args: argparse.Namespace
        The command-line arguments.
    """
    parser = ArgumentParser(
        description='Apply linguistic annotation to transcriptions.')
    parser.add_argument(
        '--corpus-dir',
        help="The directory containing XML session transcriptions.",
        default='corpus/')
    parser.add_argument('--root-file',
                        help="The name of the root file of the corpus.",
                        default="ParlaMint-RO.xml")
    parser.add_argument(
        '--taxonomy-files',
        help="Additional taxonomy files to include in annotated root file.",
        nargs='+',
        default=[
            'data/templates/ParlaMint-taxonomy-UD-SYN.ana.xml',
            'data/templates/ParlaMint-taxonomy-NER.ana.xml'
        ])
    parser.add_argument(
        '-l',
        '--log-level',
        help="The level of details to print when running.",
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        default='info')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    configure_logging(args.log_level)
    main(args.corpus_dir, args.root_file, args.taxonomy_files)
