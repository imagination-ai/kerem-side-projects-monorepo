.PHONY: install install-dev install-test build-*

ENV ?= .venv
RUN = . $(ENV)/bin/activate &&

.venv:
	virtualenv $(ENV) --python=python3.8
	touch $@

install: .venv requirements.txt
	$(RUN) pip install -r requirements.txt

install-dev: install-test
	$(RUN) pip install -r requirements-dev.txt
	$(RUN) pre-commit install && pre-commit install -t pre-push

install-test: install
	$(RUN) pip install -r requirements-test.txt

clean:
	rm -rf $(ENV)
