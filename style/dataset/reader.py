import glob
from random import shuffle
import random

import numpy as np


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
