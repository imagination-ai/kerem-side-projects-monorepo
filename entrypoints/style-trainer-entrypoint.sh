#!/usr/bin/env bash


mkdir -p /applications/style-resources/models

gsutil cp gs://projects-misc/datasets/style-datasets/book_ds.tar.gz .
tar -xzvf book_ds.tar.gz
mv book_ds style-resources/datasets/book_ds
rm -rf book_ds.tar.gz
#jupyter notebook --ip=0.0.0.0 --allow-root --no-browser --port 8080
python -m style.train.classifier_trainer
