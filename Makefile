PYTHON = python

.PHONY: all
all: build

.PHONY: build
build:
	make -C pyhdf build
	$(PYTHON) -m build

.PHONY: install
install: build
	$(PYTHON) -m pip install .

.PHONY: builddoc
.ONESHELL:
builddoc:
	export PYTHONPATH=$(shell pwd)
	$(PYTHON) install -e .
	make -C doc clean
	make -C doc html
	@echo
	@echo doc index is doc/_build/html/index.html

.PHONY: clean
test:
	$(PYTHON) -m pip install -e .
	pytest
	$(PYTHON) examples/runall.py

.PHONY: clean
clean:
	rm -rf build/ dist/ pyhdf.egg-info examples/*/*.hdf
	make -C pyhdf clean
	make -C doc clean

.PHONY: dist
dist:
	$(PYTHON) -m build
	@echo Upload to test site:
	@echo $(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	@echo Upload to PyPI:
	@echo $(PYTHON) -m twine upload dist/*
