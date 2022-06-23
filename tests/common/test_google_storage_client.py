import tempfile

import pytest
from pathlib import Path
from common.clients.google_storage_client import get_storage_client
from common.config import settings


@pytest.fixture
def storage_client(scope="module"):
    return get_storage_client(settings.MISC_BUCKET)


def test_local_storage_client_upload_source_dir_dest_dir(storage_client):
    """Test for directory destination and source are file paths."""
    content = "We've boosted the Anti-mass Spectrometer to 105%."
    with tempfile.TemporaryDirectory() as tempdirname:
        tempdirname_path = Path(tempdirname)
        fn = "testing_without_giving_name.txt"
        source_fp = tempdirname_path
        dest_fp = tempdirname_path / "style-resources"
        with open(source_fp / fn, "w") as f:
            f.write(content)
            f.flush()
            storage_client.upload(source_fp, dest_fp)
            assert open(dest_fp / fn, "r").read() == content


def test_local_storage_client_upload_source_file_dest_file(storage_client):
    """Test for destination and source are file paths."""
    content = "We've boosted the Anti-mass Spectrometer to 105%."
    with tempfile.TemporaryDirectory() as tempdirname:
        tempdirname_path = Path(tempdirname)
        fn = "testing_without_giving_name.txt"
        source_fp = tempdirname_path / fn
        dest_fp = tempdirname_path / "style-resources" / fn
        with open(source_fp, "w") as f:
            f.write(content)
            f.flush()
            storage_client.upload(source_fp, dest_fp)
            assert open(dest_fp, "r").read() == content


def test_local_storage_client_upload_source_file_dest_dir(storage_client):
    """Test for destination and source are directory paths."""
    content = "We've boosted the Anti-mass Spectrometer to 105%."
    with tempfile.TemporaryDirectory() as tempdirname:
        tempdirname_path = Path(tempdirname)
        fn = "testing_without_giving_name.txt"
        source_fp = tempdirname_path / fn
        dest_fp = tempdirname_path / "style-resources"
        with open(source_fp, "w") as f:
            f.write(content)
            f.flush()
            storage_client.upload(source_fp, dest_fp)
            assert open(dest_fp / fn, "r").read() == content
