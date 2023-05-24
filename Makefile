# Variables
VENV           = .venv
VENV_PYTHON    = $(VENV)/bin/python
SAMPLE_SIZE    = 10

# Create a sample of the corpus
.PHONY: sample
sample:
	$(VENV_PYTHON) build-corpus.py --sample --sample-size $(SAMPLE_SIZE)
	$(VENV_PYTHON) apply-linguistic-annotations.py

# Apply linguistic annotations
.PHONY: annotations
annotations:
	$(VENV_PYTHON) apply-linguistic-annotations.py
