.PHONY: install install-dev install-test build-*

ENV ?= .venv
RUN = . $(ENV)/bin/activate &&
GCS_BUCKET = test-bucket

export ENVIRONMENT=local

.venv:
	virtualenv $(ENV) --python=python3.8
	touch $@

install: .venv requirements.txt
	$(RUN) pip install -r requirements.txt

install-dev: install-test
	wget https://chromedriver.storage.googleapis.com/103.0.5005.61/chromedriver_mac64.zip
	unzip chromedriver_mac64.zip
	mv chromedriver /usr/local/bin/chromedriver
	rm chromedriver_mac64.zip

	# prep for fake gcs
	# fake buckets
	mkdir -p fake-gcs/$(GCS_BUCKET)

	touch fake-gcs/$(GCS_BUCKET)/fake-data.txt

	$(RUN) pip install -r requirements-dev.txt
	$(RUN) pre-commit install && pre-commit install -t pre-push
	brew install httpie

install-test: install
	$(RUN) pip install -r requirements-test.txt

#inflation/dataset/a101.json.gz:
#	python -m inflation.dataset_download --url "a101.com.tr/*" --output-fn $@ --type json --limit 50000
#

style-crawl:
	$(RUN) python -m style.crawler.crawl --catalog-path kerem-side-projects-monorepo/style-resources/resources/pg_catalog.csv
	make style-remove-audiobooks

style-remove-audiobooks:
	find style-resources/datasets/book_ds -name '*.txt' | xargs grep "Audio Recording Public Domain Certification" > audio.txt
	wc -l audio.txt
	echo -e "removing audio files"
	cat audio.txt | cut -f1 -d ":" | xargs rm
	rm audio.txt

style-model_training:
	$(RUN) python -m style.train.classifier_trainer --document_length 500 --cross_validation 5 --test_percentage 0.2 --min_df 3 --resampling_percentage 0.5

crawl:
	$(RUN) python -m inflation.dataset.crawl --excel-path inflation-resources/data/links.xlsx --path inflation-resources/
#inflation/dataset/%.json.gz:
#	python -m inflation.dataset_download --url ${URL} --output-fn $@ --type json --limit 1 # Update limit in the long run

clean:
	rm -rf $(ENV)

test:
	APP_RESOURCE_DIR='.' PYTHONPATH=$(PWD) pytest style-resources/tests
	PYTHONPATH=$(PWD) pytest inflation-resources/tests

format:
	 $(RUN) black -t py39 -l 80 $$(find inflation* style* common* -name "*.py")

steel-thread:
	$(RUN) python -m inflation.steel_thread --excel-path https://docs.google.com/spreadsheets/d/1_hKfQJ2DEF4TAHH3pxFCYcBgJXBYG9LZZElnF4Yf04A/edit#gid=0 --path .

e2e-test:
	bash e2e/e2e-inflation.sh
