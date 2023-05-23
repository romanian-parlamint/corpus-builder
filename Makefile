# Variables
VENV           = .venv
VENV_PYTHON    = $(VENV)/bin/python
SAMPLE_SIZE    = 50

# Create a sample of the corpus
.PHONY: sample
sample:
	$(VENV_PYTHON) build-corpus.py --sample --sample-size $(SAMPLE_SIZE)

# Apply linguistic annotations
.PHONY: annotations
annotations:
	$(VENV_PYTHON) apply-linguistic-annotations.py

