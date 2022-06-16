import pytest

from style.constants import SELECTED_AUTHORS, BASE_PATH
from style.utils.author_catalog import Book, create_catalog, is_selected_author

CATALOG_FILE_PATH = (
    BASE_PATH / "style-resources" / "resources" / "small_pg_catalog.csv"
)


@pytest.mark.parametrize(
    "case, result",
    [
        ("Dostoyevsky, Fyodor, 1821-1881", True),
        (
            "Dostoyevsky, Fyodor, 1821-1881; Hogarth, C. J., 1869-1942 [Translator]",
            True,
        ),  # Translator cases
    ],
)
def test_is_selected_author(case, result):
    book = Book("1", "title", "en", case)
    assert is_selected_author(book, SELECTED_AUTHORS) == result


def test_create_catalog():
    authors_catalog = create_catalog(CATALOG_FILE_PATH, SELECTED_AUTHORS)
    assert len(authors_catalog) == 1
