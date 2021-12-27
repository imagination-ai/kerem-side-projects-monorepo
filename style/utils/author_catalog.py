import collections
import csv
from dataclasses import dataclass
from typing import Dict

from style.constants import CATALOG_FILE_PATH, LOG_FILE_PATH, SELECTED_AUTHORS


def read_csv(filepath=CATALOG_FILE_PATH):
    lines = csv.reader(open(filepath), delimiter=",")
    next(lines)  # skip the header.
    for line in lines:
        # data has some random new lines. Replace them with white space, then strip it.
        yield list(map(lambda s: s.replace("\n", " ").strip(), line))


@dataclass
class Book:
    book_id: str
    title: str
    language: str
    author: str


def parse_data_row(row: list):
    return Book(
        row[0],  # book number
        row[3],  # title
        row[4],  # language
        row[5],  # author
    )


def is_selected_author(
    book: Book, selected_authors=SELECTED_AUTHORS, language="en"
):
    """
    Note:
        'Translator' control should check only for the second element of the strings; otherwise, there is a
    possibility that it takes the books to have multiple authors, which we are not interested in.

    book.author.split(';')[1] only controls second element for
    Args:
        book:
        selected_authors:
        language:

    Returns:

    """
    _book_author = book.author
    if ";" in book.author and "Translator" in book.author.split(";")[1]:
        book.author = book.author.split(";")[0]
    if book.author in selected_authors and book.language == language:
        book.author = _book_author
        return True
    return False


def create_catalog(
    filepath: str = CATALOG_FILE_PATH, enable_logging=True
) -> Dict:
    """

    Note:
        If there are different versions of the same book in the source catalog, it takes only the last version
    since it saves by title (the last one overwrites the previous version).


    Args:
        filepath (str): The first argument. The filepath of the source catalog of the related database.
        enable_logging (bool): It takes boolean. If it is True (Default), the function will create a log file.
    Returns:

        Return a dictionary contains authors' dictionaries that contain book title and book id pairs.

    """
    author_book_catalog = collections.defaultdict(list)
    for row in read_csv(filepath):
        book = parse_data_row(row)
        if is_selected_author(book):
            if enable_logging:
                create_control_file(book)
            if ";" in book.author:
                book.author = book.author.split(";")[0]
            author_book_catalog[book.author].append(book)

    return author_book_catalog


def create_control_file(book: Book, filepath: str = LOG_FILE_PATH):
    """
    It records the selected book entries taken from Gutenberg's Catalog. It saves the entries as how
    they were in the Gutenberg catalog.

    Args:
        book (Book):
        filepath (str): The argument shows where the file will save.

    Returns:
        None
    """
    with open(filepath, "a") as f:
        f.write(f"{book.book_id} {book.author}  {book.title}")
        f.write("\n")
