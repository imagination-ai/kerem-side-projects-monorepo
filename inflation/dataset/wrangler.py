import _pickle as cPickle
from inflation.dataset.reader import (
    InflationJSONA101DatasetReader,
    InflationDataset,
)
from pathlib import Path
import pandas as pd

FILE_DIR_PATH = Path(__file__).parents[2] / "inflation-resources/data/"


def save_dataset(dataset: InflationDataset, output_file_name):
    """
    It saves InflationJSONA101DatasetReader records by serializing.
    """
    full_path = FILE_DIR_PATH / output_file_name

    with open(full_path, "wb") as f:
        cPickle.dump(dataset, f)


def read_dataset(file_path):
    with open(file_path, "rb") as input_file:
        return cPickle.load(input_file)


def convert_dataset_to_dataframe(dataset):
    return pd.DataFrame([line.__dict__ for line in dataset])


def run():
    print(FILE_DIR_PATH)


if __name__ == "__main__":
    run()
