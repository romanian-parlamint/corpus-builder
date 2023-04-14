# ParlaMint-RO corpus builder #

This repository contains the code required for building the `ParlaMint-RO` corpus.

Each script in the root of this repository represents a step in the processing pipeline. Theese scripts can be classified as follows:

## Prepreprocessing scripts ##

- [`build-speakers-list.py`](./build-speakers-list.py) - iterates through session transcripts in `JSON` format and builds a list of unique speaker names, which is then saved to a `CSV` file.
- [`classify-speakers.py`](./classify-speakers.py) - iterates through session transcripts in `JSON` format and classifies speakers into MPs and invited speakers; the lists are saved in `CSV` format.

## Corpus building script ##

The script to build the corpus is [`build-corpus.py`](./build-corpus.py).
