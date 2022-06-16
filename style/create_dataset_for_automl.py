import csv

from style.dataset.reader import DatasetReader
from style.constants import FILE_PATH_BOOK_DS, FILE_PATH_AUTOML_DS
from os import mkdir, path


def create_automl_dataset(
    ds_name,
    num_of_books=None,
    output_dir_path=FILE_PATH_AUTOML_DS,
    book_ds_dir_path=FILE_PATH_BOOK_DS,
    chunk_size=500,
):
    if not path.isdir(output_dir_path):
        mkdir(output_dir_path)
    dataset = DatasetReader.load_files(
        book_ds_dir_path, chunk_size, num_of_books
    )
    ds_name += ".csv"
    ds_path = path.join(output_dir_path, ds_name)

    with open(ds_path, "w", encoding="UTF8") as f:
        header = ["text_items", "labels"]
        writer = csv.writer(f)
        writer.writerow(header)
        for chunk, target in zip(dataset.data, dataset.target):
            writer.writerow([chunk, target])


def run():
    create_automl_dataset(
        "automl_style_ds_full-chunk_size", num_of_books=20, chunk_size=20000
    )


if __name__ == "__main__":
    run()
