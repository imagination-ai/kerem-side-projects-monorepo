import os
from pathlib import Path
from unittest import mock

import pytest

from style.crawler.crawl import GutenbergWrangler

STYLE_RESOURCES_PATH = Path(
    os.getenv("APP_RESOURCE_DIR", Path(__file__).parents[3])
)


@pytest.fixture(scope="function")
def gutenberg_wrangler():
    return GutenbergWrangler("http://aleph.gutenberg.org")


@pytest.fixture(scope="function")
def html_test_file():
    import codecs

    fp = STYLE_RESOURCES_PATH / "resources" / "test_page.html"
    return codecs.open(fp, "r").read()


class TestGutenbergWrangler:
    @pytest.mark.parametrize(
        "case, result",
        [
            ("2", "http://aleph.gutenberg.org/0/2/2.txt"),
            ("12", "http://aleph.gutenberg.org/1/12/12.txt"),
            ("231", "http://aleph.gutenberg.org/2/3/231/231.txt"),
            ("5000", "http://aleph.gutenberg.org/5/0/0/5000/5000.txt"),
            ("12325", "http://aleph.gutenberg.org/1/2/3/2/12325/12325.txt"),
        ],
    )
    def test_transform_book_id_full_url(self, gutenberg_wrangler, case, result):
        assert gutenberg_wrangler.transform_book_id_to_url(case) == result

    @pytest.mark.parametrize(
        "case", ("", "12412356")
    )  # Test1: For Empty string case, Test2: Out of range case
    def test_get_book_id_url_error(self, gutenberg_wrangler, case):
        """Test NotImplemented Error for get_book_full_error function"""
        with pytest.raises(ValueError):
            gutenberg_wrangler.transform_book_id_to_url(case)

    @mock.patch("style.crawler.crawl.requests.Session.get")
    def test_get_book_status_code_200(
        self, mock_requests_get, gutenberg_wrangler
    ):
        """
        Todo:
            - Dogru dosyayi cekiyor mu?
            - Dogru pathe kaydediyor mu?
            - 505 ve diger caseler icin mock testler yazilacak
            - 404'e gidiyor mu?
            - 404'e gittikten sonra .txt dosyasi bulmakta basarili mi?
        """
        mock_requests_get.return_value = mock.Mock(status_code=200, text="TEXT")
        #        requests.Session.get.call_count  # Q: bu niye gozukmuyor?
        assert gutenberg_wrangler.get_book("2") == "TEXT"
        mock_requests_get.assert_called_once()

    @mock.patch("style.crawler.crawl.requests.Session.get")
    def test_get_book_status_code_404(
        self, mock_requests_get, gutenberg_wrangler, html_test_file
    ):
        mock_requests_get.return_value = mock.Mock(
            status_code=404, content=html_test_file, text="The correct one"
        )
        assert gutenberg_wrangler.get_book("44") == "The correct one"
