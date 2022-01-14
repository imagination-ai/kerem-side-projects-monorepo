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

download-dataset:
	python -m inflation.dataset_download --url "a101.com.tr/*" --output-fn a101.json.gz --type json --limit 1 # Update limit in the long run

clean:
	rm -rf $(ENV)
