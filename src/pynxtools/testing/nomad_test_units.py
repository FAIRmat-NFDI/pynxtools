import pytest
from nomad.files import DirectoryObject, StaginUploadFiles, UploadFiles


# TODO: get the example_name according the example comes from different pynxtools reader.
@pytest.mark.parametrize("example_name", ["stm"])
@pytest.fixture(scope="function")
def create_upload_id(example_name):
    """Create upload id for test purpose."""
    # Create os path
    upload_base_dir = DirectoryObject(StaginUploadFiles.base_folder_for(example_name))

    # Delete dir if the directory in that path exists already
    if upload_base_dir.exists():
        upload_base_dir.delete()

    yield example_name
    # Delete upload directory once test is done with the upload id
    if upload_base_dir.exists():
        upload_base_dir.delete()


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


def test_compare_archive_json_file():
    """Compare the json file generated from yaml file."""
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
