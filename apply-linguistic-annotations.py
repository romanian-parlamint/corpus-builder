#!/usr/bin/env python
"""Perform linguistic annotation on the corpus."""
from argparse import ArgumentParser
from argparse import Namespace
from framework.core.linguisticannotation.componentannotator import CorpusComponentAnnotator
from framework.core.linguisticannotation.corpusiterator import CorpusIterator
from framework.core.linguisticannotation.linguisticannotator import LinguisticAnnotator
from framework.core.xmlstats import XmlTagCountWriter
from framework.core.xmlstats import XmlTagCounter
from framework.core.xmlutils import XmlElements
from framework.utils.loggingutils import configure_logging


def main(corpus_dir: str):
    """Entry point of the module.

    Parameters
    ----------
    corpus_dir: str, required
        The directory containing XML transcript files.
    """
    iterator = CorpusIterator(corpus_dir)
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
    for component_file in iterator.iter_corpus_files():
        annotator = CorpusComponentAnnotator(component_file,
                                             linguistic_annotator)
        annotator.apply_annotation()
        counter = XmlTagCounter(component_file)
        count_writer = XmlTagCountWriter(component_file, tag_map)
        count_writer.update_tage_usage(counter.get_tag_counts())
        count_writer.save_changes()


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
    main(args.corpus_dir)

# text = """Stimaţi colegi,
# Bună dimineaţa.
# Începem lucrările noastre de astăzi.
# Rog şefii grupurilor parlamentare să invite pe colegi în sală şi, până atunci, vă rog să-mi permiteţi să vă informez cu privire la legile depuse la secretarii generali ai Camerei Deputaţilor şi În Lege pentru ratificarea Convenţiei privind accesul la informaţie, participarea publicului la luarea deciziei şi accesul la justiţie în probleme de mediu, semnată la Aarhus la 25 iunie 1998;
# Lege pentru ratificarea Protocolului de adaptare a aspectectelor instituţionale ale Acordului european instituind o asociere între România, pe de o parte, şi comunităţile europene şi statele membre Lege pentru ratificarea Acordului european asupra transferului responsabilităţii cu privire la refugiaţi, adoptat la Strasbourg la 16 octombrie 1980;
# Lege pentru ratificarea Acordului privind conservarea păsărilor de apă migratoare african-euroasiatice, adoptat la Haga la 16 iunie 1995;
# Lege pentru aderarea României la Acordul privind conservarea liliecilor în Europa, adoptat la Londra în 4 decembrie 1991;
# Lege pentru ratificarea Acordului privind conservarea cetaceelor din Marea Neagră, Marea Mediterană şi din Zona contiguă a Atlanticului, adoptat la Monaco la 24 noiembrie 1996;
# Lege privind aprobarea Ordonanţei de urgenţă a Guvernului nr.97/1999 pentru modificarea Legii nr.8/1994 privind constituirea şi utilizarea Fondului special pentru dezvoltarea şi modernizarea Lege Lege pentru aprobarea Ordonanţei de urgenţă a Guvernului nr.175/1999 privind înfiinţarea Agenţiei pentru organizarea Centrului Regional pentru Prevenirea şi Combaterea Infracţionalităţii
# Acestea sunt deci legile în termenul regulamentar şi domnii deputaţi sau senatori care vor să sesizeze Curtea Constituţională pot să o facă."""
# sentence_splitter = SentenceSplitter()
# annotator = LinguisticAnnotator()
# for sentence in sentence_splitter.split(text):
#     print(sentence)
#     doc, conll_df = annotator.annotate(sentence)
#     print("LINGUISTIC ANNOTATION")
#     print(conll_df)
#     print("NAMED ENTITY IDENTIFICATION")
#     for ne_span in doc.ents:
#         print([token.text for token in ne_span], ne_span.label_)
