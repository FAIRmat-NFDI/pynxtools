"""Generic test for reader plugins."""

from typing import Literal

import logging
import os
from glob import glob

from pynxtools.dataconverter.helpers import get_nxdl_root_and_path
from pynxtools.dataconverter.convert import get_reader, transfer_data_into_template
from pynxtools.dataconverter.validation import validate_dict_against
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

    def __init__(self, nxdl, reader_name, files_or_dir, tmp_path, caplog) -> None:
        """Initialize the test object.

        Parameters
        ----------
        nxdl : str
            Name of the NXDL application definition that is to be tested by this reader plugin (e.g. NXsts, NXmpes, etc).
        reader_name : str
            The name of the reader class (e.g. stm, mpes, xps, ...) to be tested.
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
        self.reader_name = reader_name
        self.reader = get_reader(self.reader_name)
        self.files_or_dir = files_or_dir
        self.ref_nexus_file = ""
        self.tmp_path = tmp_path
        self.caplog = caplog
        self.created_nexus = f"{tmp_path}/{os.sep}/output.nxs"

    def convert_to_nexus(
        self,
        caplog_level: Literal["ERROR", "WARNING"] = "ERROR",
        ignore_undocumented: bool = False,
    ):
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

        nxdl_root, nxdl_file = get_nxdl_root_and_path(self.nxdl)
        assert os.path.exists(nxdl_file), f"NXDL file {nxdl_file} not found"

        read_data = transfer_data_into_template(
            input_file=input_files,
            reader=self.reader_name,
            nxdl_name=self.nxdl,
            nxdl_root=nxdl_root,
            skip_verify=True,
        )

        # Clear the log of `transfer_data_into_template`
        self.caplog.clear()

        with self.caplog.at_level(caplog_level):
            _ = validate_dict_against(
                self.nxdl, read_data, ignore_undocumented=ignore_undocumented
            )
        assert self.caplog.text == ""

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
