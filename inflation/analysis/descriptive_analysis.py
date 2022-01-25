import numpy as np


def calculate_missing_in_stocks(df):
    """TODO: assign variable repetitive objects"""
    return (
        f"{len(df[df['in_stock'] == True])} items in stocks in total of {len(df)} items.",
        f"{round(len(df[df['in_stock'] == True]) / len(df), 4) * 100}% of products in the stock.",
    )


def get_number_of_unique_entries(df):
    """Get number of unique entries in each column with categorical data
    It returns number of unique entries by column, in ascending order
    """
    object_cols = [col for col in df.columns if df[col].dtype == "object"]
    object_nunique = list((map(lambda col: df[col].nunique(), object_cols)))
    d = dict(zip(object_cols, object_nunique))

    return sorted(d.items(), key=lambda x: x[1])


def missing_values_by_column(df):
    missing_values_count = df.isnull().sum()

    total_missing = missing_values_count.sum()
    total_cells = np.product(df.shape)
    percent_missing = total_missing / total_cells * 100

    return (
        missing_values_count,
        f"Total number of missing data points: {total_missing},"
        f"{percent_missing}% of data is missing",
    )
