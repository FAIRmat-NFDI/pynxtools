"""Generic test for reader plugins."""

import importlib.metadata as importlib_metadata
import logging
import os
from glob import glob

import toml

from pynxtools.dataconverter.convert import get_nxdl_root_and_path
from pynxtools.dataconverter.helpers import (
    generate_template_from_nxdl,
    validate_data_dict,
)
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.writer import Writer
from pynxtools.nexus import nexus


def get_log_file(nxs_file, log_file, tmp_path):
    """Get log file for the nexus file with read_nexus tools."""
    logger = logging.getLogger(__name__)
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    log_file = os.path.join(tmp_path, log_file)
    handler = logging.FileHandler(log_file, "w")
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = nexus.HandleNexus(logger, nxs_file, None, None)
    nexus_helper.process_nexus_master_file(None)
    return log_file


class ReaderTest:
    """Generic test for reader plugins."""

    def __init__(self, nxdl, reader, files_or_dir, tmp_path, caplog) -> None:
        """Initialize the test object.

        Parameters
        ----------
        nxdl : str
            Name of the NXDL application definition that is to be tested by this reader plugin (e.g. NXsts, NXmpes, etc).
        reader : class
            The reader class (e.g. STMReader, MPESReader) to be tested.
        files_or_dir : str
            List of input files or full path string to the example data directory that contains all the files
            required for running the data conversion through the reader.
        ref_nexus_file : str
            Full path string to the reference NeXus file generated from the same
            set of input files.
        tmp_path : pathlib.PosixPath
            Pytest fixture variable, used to clean up the files generated during the test.
        caplog : _pytest.logging.LogCaptureFixture
            Pytest fixture variable, used to capture the log messages during the test.
        """

        self.nxdl = nxdl
        self.reader = reader
        self.files_or_dir = files_or_dir
        self.ref_nexus_file = ""
        self.tmp_path = tmp_path
        self.caplog = caplog
        self.created_nexus = f"{tmp_path}/{os.sep}/output.nxs"

    def convert_to_nexus(self):
        """
        Test the example data for the reader plugin.
        """

        assert hasattr(
            self.reader, "supported_nxdls"
        ), f"Reader{self.reader} must have supported_nxdls attribute"
        assert callable(self.reader.read), f"Reader{self.reader} must have read method"

        if isinstance(self.files_or_dir, (list, tuple)):
            example_files = self.files_or_dir
        else:
            example_files = sorted(glob(os.path.join(self.files_or_dir, "*")))
        self.ref_nexus_file = [file for file in example_files if file.endswith(".nxs")][
            0
        ]
        input_files = [file for file in example_files if not file.endswith(".nxs")]
        assert self.ref_nexus_file, "Reference nexus (.nxs) file not found"
        assert (
            self.nxdl in self.reader.supported_nxdls
        ), f"Reader does not support {self.nxdl} NXDL."

        root, nxdl_file = get_nxdl_root_and_path(self.nxdl)
        assert os.path.exists(nxdl_file), f"NXDL file {nxdl_file} not found"
        template = Template()
        generate_template_from_nxdl(root, template)

        read_data = self.reader().read(
            template=Template(template), file_paths=tuple(input_files)
        )

        assert isinstance(read_data, Template)
        with self.caplog.at_level("ERROR", "WARNING"):
            is_success = validate_data_dict(template, read_data, root)
        assert is_success, "Validation failed"
        for record in self.caplog.records:
            if record.levelname == "ERROR":
                assert False, record.message
        Writer(read_data, nxdl_file, self.created_nexus).write()

    def check_reproducibility_of_nexus(self):
        """Reproducibility test for the generated nexus file."""
        ref_log = get_log_file(self.ref_nexus_file, "ref_nexus.log", self.tmp_path)
        gen_log = get_log_file(self.created_nexus, "gen_nexus.log", self.tmp_path)
        with open(gen_log, "r", encoding="utf-8") as gen, open(
            ref_log, "r", encoding="utf-8"
        ) as ref:
            gen_lines = gen.readlines()
            ref_lines = ref.readlines()
        if len(gen_lines) != len(ref_lines):
            assert False, "Log files are different"
        for ind, (gen_l, ref_l) in enumerate(zip(gen_lines, ref_lines)):
            if gen_l != ref_l:
                # skip version conflicts
                if gen_l.startswith("DEBUG - value: v") and ref_l.startswith(
                    "DEBUG - value: v"
                ):
                    continue
                assert False, (
                    f"Log files are different at line {ind}"
                    f" generated: {gen_l} \n referenced : {ref_l}"
                )


class NeXusParserInNomadTest:
    """Generic test for reader plugins."""

    def __init__(self, nx_f_path, caplog) -> None:
        """Initialize the test object.
        parameters
        ----------
        nx_f_path : str
            Full path string to the NeXus file that is to be tested.
        caplog : _pytest.logging.LogCaptureFixture
        """
        try:
            from nomad.datamodel import EntryArchive
            from nomad.parsing.nexus import NexusParser
        except ImportError:
            raise ImportError("Nomad-lab is not installed in python env.")

        self.nx_f_path = nx_f_path
        self.caplog = caplog

    def verfy_nxs_file_with_nexus_parser(self):
        """Test the NeXus file with nexus parser."""
        archive = EntryArchive()
        example_data = "tests/data/parsers/nexus/SiO2onSi.ellips.nxs"
        NexusParser().parse(example_data, archive, self.caplog)
        archive.m_to_dict(with_out_meta=True)


def get_package_version(package_name):
    """Read the version from installed packages."""
    try:
        version = importlib_metadata.version(package_name)
        return version
    except importlib_metadata.PackageNotFoundError:
        return None


def get_classifier_catagory_versions(toml_file, classifier_key):
    """Get the classifier category for the test.

    Parameters
    ----------
    toml_file : str
        Path to the toml file.
    classifier_key : str
        Classifier key to get the version (e.g. Programming Language :: Python,
        License :: OSI Approved).
    """
    version_ls = []
    with open(toml_file, "r", encoding="utf-8") as f:
        data = toml.load(f)
    classfier_ls = data["project"]["classifiers"]
    for classifier in classfier_ls:
        if classifier.startswith(classifier_key):
            version = classifier.split(classifier_key.strip() + " ::")[-1]
            version_ls.append(version.strip())
    return version_ls


def verify_package_version(toml_file, package_name, classifier_key):
    """Test to verify the package version."""
    pkg_version = get_package_version(package_name)
    versions_tml = get_classifier_catagory_versions(toml_file, classifier_key)
    has_right_version = False
    for version in versions_tml:
        if pkg_version.startswith(version):
            has_right_version = True
    assert (
        has_right_version
    ), f"{package_name} version {pkg_version} not found in {versions_tml}"


def test_verfy_pynxtools_version(toml_file, pynx_key="Pynxtools ::"):
    """Test to verify the pynxtools version."""
    verify_package_version(toml_file, "pynxtools", pynx_key)


def test_verfy_nomad_version(toml_file, nomad_key="Nomad-Lab ::"):
    """Test to verify the nomad version."""
    verify_package_version(toml_file, "nomad-lab", nomad_key)
