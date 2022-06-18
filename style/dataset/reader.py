from collections import Counter
import datetime
import glob
from pathlib import Path
import random
from random import shuffle
import tempfile

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common.clients.google_storage_client import get_storage_client
from common.config import settings


class DatasetReader:
    @staticmethod
    def load_files(container_path, n: int = 500, num_of_books=None):
        """Load book files with author names as categories via subfolder names.

        It assumes container folders stored a two levels folder structure such as the following
            container_folder/
                author_1_folder/
                    book_1.txt
                    book_30.txt
                ...
                author_8_folder/
                    book_40.txt
                  book_55.txt
        Args:
            n: split the books by n.
            container_path:

        Returns:

        """
        # authors' names are label at the same time folder names
        filenames = sorted(
            glob.glob(f"{container_path}/*/*.txt", recursive=True)
        )

        if num_of_books is not None:
            filenames = filenames[:num_of_books]

        data = []
        target = []
        for filename in filenames:
            with open(filename, "r") as f:
                text = f.read().split()
                author = filename.split("/")[-2]
                for i in range(0, len(text), n):
                    data.append(" ".join(text[i : i + n]))
                    target.append(author)

        return Dataset(data, target)


class Dataset:
    def __init__(self, data, target):
        assert len(data) == len(target)
        self._data = data
        self._target = target

    @property
    def target(self):
        return self._target

    @property
    def data(self):
        return self._data

    def __len__(self):
        return len(self._data)

    def shuffle(self, seed: int = 123):
        data = np.array(self._data)
        target = np.array(self._target)
        indices = list(range(0, len(self)))
        random.seed(seed)
        shuffle(indices)
        self._data = []
        self._target = []
        for i in indices:
            self._data.append(data[i])
            self._target.append(target[i])

    def __getitem__(self, s):
        if isinstance(s, slice):
            return Dataset(self.data[s], self.target[s])

        return Dataset([self.data[s]], [self.target[s]])

    def resample(self, percentage: float):
        assert 0 < percentage <= 1.0
        """
        It takes sub sample of the dataset. First, randomized the sorted dataset.


        Args:
            percentage: It takes percentage piece from data. It takes

        Returns:

        """
        if percentage != 1.0:
            self.shuffle()
            size = len(self.data)
            new_dataset_size = round(size * percentage)
            return self[:new_dataset_size]
        else:
            return self


def draw_sample_distributions(
    dataset1: Dataset, dataset2: Dataset, dataset1_label, dataset2_label
):
    """
    It is a function that helps to compare how two different samples are distributed.
    It saves the figures.
    Returns: None

    """

    misc_client = get_storage_client(bucket_name=settings.MISC_BUCKET)

    dataset1_prop_val = calculate_author_distributions(dataset1)
    dataset2_prop_val = calculate_author_distributions(dataset2)

    # transform to df to merge and draw its figure
    df1 = pd.DataFrame(
        dataset1_prop_val.items(), columns=["author", f"{dataset1_label}_share"]
    )
    df2 = pd.DataFrame(
        dataset2_prop_val.items(), columns=["author", f"{dataset2_label}_share"]
    )

    df_merged = pd.merge(df1, df2, how="outer", on="author")

    df_merged.plot.barh(
        rot=0,
        x="author",
        color={
            f"{dataset1_label}_share": "blue",
            f"{dataset2_label}_share": "red",
        },
        figsize=(15, 30),
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        suffix = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        fn = f"distribution-comparison-{suffix}.svg"
        plt.savefig(tmpdir_path / fn)
        return misc_client.upload(
            tmpdir_path / fn, f"style/figures/{fn}", enable_public=False
        )


def calculate_author_distributions(dataset: Dataset):
    """
    It takes a Dataset and returns the proportional value representing each author in the dataset.
    Args:
        dataset:

    Returns:

    """
    counts = Counter(dataset.target)
    total_count = sum(counts.values())

    return {
        author: round(count / total_count, 3)
        for (author, count) in counts.items()
    }
