from collections import Counter

import pytest

from style.constants import FILE_PATH_MOCK_DS
from style.dataset.reader import (
    DatasetReader,
    calculate_author_distributions,
    draw_sample_distributions,
)
import tempfile


@pytest.fixture(scope="module")
def dataset():
    return DatasetReader.load_files(FILE_PATH_MOCK_DS, 500)


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
    with pytest.raises(AssertionError):
        assert len(dataset.resample(percentage=0))
        assert len(dataset.resample(percentage=3))


def test_resample_as_balanced_sampling(dataset):
    num_doc = 27
    resampled_dataset = dataset.resample_balanced(num_doc)

    counts = Counter(resampled_dataset.target)
    assert len(resampled_dataset.target) != 0

    for v in counts.values():
        assert v == num_doc

    assert "abraham_lincoln" not in set(resampled_dataset.target)

    num_doc = 26
    resampled_dataset = dataset.resample_balanced(num_doc)
    assert "abraham_lincoln" in set(resampled_dataset.target)


def test_calculate_author_distributions(dataset):
    dist = calculate_author_distributions(dataset)
    assert isinstance(dist, dict)
    assert abs(sum(dist.values())) - 1 < 0.0001


def test_draw_sample_distributions(dataset):
    dataset_sampled = dataset.resample(0.2)
    with tempfile.TemporaryDirectory() as tmpdirname:
        path = draw_sample_distributions(
            dataset, dataset_sampled, "label_full", "label_sampled", tmpdirname
        )
    assert str(path).endswith(".svg")
