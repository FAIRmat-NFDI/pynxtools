import pytest


@pytest.fixture(scope="function")
def create_upload_id():
    """Create upload id for test purpose."""
    ...


@pytest.fixture(scope="function")
def add_raw_files_to_test_upload():
    """Include test files to the upload dir."""
    ...


def test_upload_files():
    """Test if files are included in upload folder."""
    ...


def test_run_processing_on_schema():
    """Run the processing function on schema file (schema.archive.yaml)."""
    ...


def test_nxs_file_is_generated():
    """Check if nexus file has been created."""
    ...


def test_parse_nxs_file():
    """Parse nexus file."""
    ...


def test_metainfo_generation_from_nexus_file():
    """Check if metainfo has been generated from nexus file properly.
    TODO: Ensure if this part parsing metadata in elastic search. Usually
        this automatically include data curation in elastic search service.
    """
    ...


def test_upload_in_properly_deleted():
    """Delete the upload after finishing the test."""
    ...
