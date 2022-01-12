from dataclasses import dataclass
from datetime import datetime


class BaseJSONDataReader:
    def read(self, filename, columns=None):
        raise NotImplementedError()


class InflationJSONDatasetReader(BaseJSONDataReader):
    def read(self, filename, fields=None):
        """It goes through the `filename` and create InflationRecords

        Args:
            filename:
            fields: fields to include. If it is None, include everything.

        Returns:

        """
        # TODO (kerem)
        pass
        # return InflationData(data)


class InflationDataRecord(dataclass):
    price: float
    currency: str
    item: str  # item identifier for this data.
    sample_date: datetime  # price was valid for this date.
    # ...


class InflationDataset:
    def __init__(self, data):
        self.dataset = data

    def __iter__(self):
        # TODO (kerem)
        pass

    def __get__(self, idx):
        return self.dataset[idx]

    def __len__(self):
        return len(self.dataset)
