import pytest

from style.constants import FILE_PATH_MOCK_DS
from style.dataset.reader import DatasetReader


@pytest.fixture
def dataset():
    return DatasetReader.load_files(FILE_PATH_MOCK_DS)


class TestDatasetReader:
    def test_load_files(self, dataset):
        assert dataset.target[0] == "frederick_douglass"
        assert len(dataset.data) == 571


class TestDataset:
    def test_slice(self, dataset):
        small_dataset = dataset[:2]
        assert len(small_dataset) == 2
        assert dataset[0].target == ["frederick_douglass"]
