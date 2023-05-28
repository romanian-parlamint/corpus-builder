# Variables
VENV           = .venv
VENV_PYTHON    = $(VENV)/bin/python
SAMPLE_SIZE    = 10

apply_annotations=($(VENV_PYTHON) apply-linguistic-annotations.py)
# Create a sample of the corpus
.PHONY: sample
sample:
	$(VENV_PYTHON) build-corpus.py --sample --sample-size $(SAMPLE_SIZE)
	$(call apply_annotations)

# Apply linguistic annotations
.PHONY: annotations
annotations:
	$(call apply_annotations)

# Create the corpus
.PHONY: corpus
corpus:
	$(VENV_PYTHON) build-corpus.py
	$(call apply_annotations)

