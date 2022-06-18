import pytest

from style.constants import FILE_PATH_MOCK_DS
from style.dataset.reader import DatasetReader, calculate_author_distributions


@pytest.fixture
def dataset():
    return DatasetReader.load_files(FILE_PATH_MOCK_DS)


class TestDatasetReader:
    def test_load_files(self, dataset):
        assert dataset.target[0] == "abraham_lincoln"
        assert len(dataset.data) == 571


class TestDataset:
    def test_slice(self, dataset):
        small_dataset = dataset[:2]
        assert len(small_dataset) == 2
        assert dataset[0].target == ["abraham_lincoln"]


def test_resample(dataset):
    assert len(dataset.resample(percentage=0.5)) == 286
    assert len(dataset.resample(percentage=0.2)) == 114
    assert len(dataset.resample(percentage=1)) == 571
    assert len(dataset.resample(percentage=0)) == 0


def test_calculate_author_distributions(dataset):
    dist = calculate_author_distributions(dataset)
    assert isinstance(dist, dict)
    assert abs(sum(dist.values())) - 1 < 0.0001
