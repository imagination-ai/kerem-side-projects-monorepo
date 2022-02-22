import pytest

from style.constants import SELECTED_AUTHORS
from style.utils.author_catalog import Book, create_catalog, is_selected_author


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
    assert is_selected_author(book) == result


def test_create_catalog():
    authors_catalog = create_catalog()
    assert len(authors_catalog) == len(SELECTED_AUTHORS)
