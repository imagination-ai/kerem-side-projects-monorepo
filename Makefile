.PHONY: install install-dev install-test build-*

ENV ?= .venv
RUN = . $(ENV)/bin/activate &&
GCS_BUCKET = test-bucket

.venv:
	virtualenv $(ENV) --python=python3.8
	touch $@

install: .venv requirements.txt
	$(RUN) pip install -r requirements.txt

install-dev: install-test
	wget https://chromedriver.storage.googleapis.com/98.0.4758.102/chromedriver_mac64.zip
	unzip chromedriver_mac64.zip
	mv chromedriver /usr/local/bin/chromedriver

	# prep for fake gcs
	mkdir -p fake-gcs/$(GCS_BUCKET)
	touch fake-gcs/$(GCS_BUCKET)/fake-data.txt

	$(RUN) pip install -r requirements-dev.txt
	$(RUN) pre-commit install && pre-commit install -t pre-push

install-test: install
	$(RUN) pip install -r requirements-test.txt

#inflation/dataset/a101.json.gz:
#	python -m inflation.dataset_download --url "a101.com.tr/*" --output-fn $@ --type json --limit 50000

crawl:
	$(RUN) python -m inflation.dataset.crawl --excel-path inflation-resources/data/links.xlsx --path inflation-resources/
#inflation/dataset/%.json.gz:
#	python -m inflation.dataset_download --url ${URL} --output-fn $@ --type json --limit 1 # Update limit in the long run

train-model-small:
	APP_RESOURCE_DIR=style-resources $(RUN) python -m style.train.classifier_trainer --model-name small --train-data-size 200

clean:
	rm -rf $(ENV)

test:
	APP_RESOURCE_DIR='style-resources' PYTHONPATH=$(PWD) pytest style-resources/tests
	PYTHONPATH=$(PWD) pytest inflation-resources/tests

format:
	 $(RUN) black -t py39 -l 80 $$(find inflation* style* common* -name "*.py")

steel-thread:
	$(RUN) python -m inflation.steel_thread --excel-path https://docs.google.com/spreadsheets/d/1_hKfQJ2DEF4TAHH3pxFCYcBgJXBYG9LZZElnF4Yf04A/edit#gid=0 --path .
