#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Generic test for reader plugins."""

import logging
import os
from glob import glob
from typing import List, Literal, Tuple, Dict

try:
    from nomad.client import parse

    NOMAD_AVAILABLE = True
except ImportError:
    NOMAD_AVAILABLE = False


from pynxtools.dataconverter.convert import get_reader, transfer_data_into_template
from pynxtools.dataconverter.helpers import (
    add_default_root_attributes,
    get_nxdl_root_and_path,
)
from pynxtools.dataconverter.validation import validate_dict_against
from pynxtools.dataconverter.writer import Writer
from pynxtools.nexus.nexus import HandleNexus


def get_log_file(nxs_file, log_file, tmp_path):
    """Get log file for the nexus file with read_nexus tools."""
    logger = logging.getLogger("pynxtools")
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    log_file = os.path.join(tmp_path, log_file)
    handler = logging.FileHandler(log_file, "w")
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = HandleNexus(logger, nxs_file, None, None)
    nexus_helper.process_nexus_master_file(None)
    return log_file


class ReaderTest:
    """Generic test for reader plugins."""

    def __init__(
        self, nxdl, reader_name, files_or_dir, tmp_path, caplog, **kwargs
    ) -> None:
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
        kwargs : Dict[str, Any]
            Any additional keyword arguments to be passed to the readers' read function.
        """

        self.nxdl = nxdl
        self.reader_name = reader_name
        self.reader = get_reader(self.reader_name)

        self.files_or_dir = files_or_dir
        self.ref_nexus_file = ""
        self.tmp_path = tmp_path
        self.caplog = caplog
        self.created_nexus = f"{tmp_path}/{os.sep}/output.nxs"
        self.kwargs = kwargs

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
            **self.kwargs,
        )

        # Clear the log of `transfer_data_into_template`
        self.caplog.clear()

        with self.caplog.at_level(caplog_level):
            _ = validate_dict_against(
                self.nxdl, read_data, ignore_undocumented=ignore_undocumented
            )
        assert self.caplog.text == ""

        add_default_root_attributes(
            data=read_data, filename=os.path.basename(self.created_nexus)
        )
        Writer(read_data, nxdl_file, self.created_nexus).write()

        if NOMAD_AVAILABLE:
            kwargs = dict(
                strict=True,
                parser_name=None,
                server_context=False,
                username=None,
                password=None,
            )

            parse(self.created_nexus, **kwargs)

    def check_reproducibility_of_nexus(self, **kwargs):
        """Reproducibility test for the generated nexus file."""
        reader_ignore_lines: List[str] = kwargs.get("ignore_lines", [])
        reader_ignore_sections: Dict[str, List[str]] = kwargs.get("ignore_sections", {})

        IGNORE_LINES: List[str] = reader_ignore_lines + [
            "DEBUG - value: v",
            "DEBUG - value: https://github.com/FAIRmat-NFDI/nexus_definitions/blob/",
            "DEBUG - ===== GROUP (// [NXroot::]):",
        ]
        IGNORE_SECTIONS: Dict[str, List[str]] = {
            **reader_ignore_sections,
            "ATTRS (//@HDF5_version)": ["DEBUG - value:"],
            "ATTRS (//@file_name)": ["DEBUG - value:"],
            "ATTRS (//@file_time)": ["DEBUG - value:"],
            "ATTRS (//@file_update_time)": ["DEBUG - value:"],
            "ATTRS (//@h5py_version)": ["DEBUG - value:"],
        }

        SECTION_SEPARATOR = "DEBUG - ===== "

        def should_skip_line(gen_l: str, ref_l: str, ignore_lines: List[str]) -> bool:
            """Check if both lines start with any ignored prefix."""
            return any(
                gen_l.startswith(ignore) and ref_l.startswith(ignore)
                for ignore in ignore_lines
            )

        def load_logs(
            gen_log_path: str, ref_log_path: str
        ) -> Tuple[List[str], List[str]]:
            """Load log files and return their contents as lists of lines."""
            with open(gen_log_path, "r", encoding="utf-8") as gen, open(
                ref_log_path, "r", encoding="utf-8"
            ) as ref:
                return gen.readlines(), ref.readlines()

        def compare_logs(gen_lines: List[str], ref_lines: List[str]) -> None:
            """Compare log lines, ignoring specific differences."""
            if len(gen_lines) != len(ref_lines):
                raise AssertionError(
                    f"Log files are different: mismatched line counts. "
                    f"Generated file has {len(gen_lines)} lines, "
                    f"while reference file has {len(ref_lines)} lines."
                )

            section_ignore_lines = []
            section = None
            for ind, (gen_l, ref_l) in enumerate(zip(gen_lines, ref_lines)):
                if gen_l.startswith(SECTION_SEPARATOR) and ref_l.startswith(
                    SECTION_SEPARATOR
                ):
                    section = gen_l.rsplit(SECTION_SEPARATOR)[-1].strip()
                    section_ignore_lines = IGNORE_SECTIONS.get(section, [])

                # Compare lines if not in ignore list
                if gen_l != ref_l and not should_skip_line(
                    gen_l, ref_l, IGNORE_LINES + section_ignore_lines
                ):
                    raise AssertionError(
                        f"Log files are different at line {ind}\n"
                        f"generated: {gen_l}\nreferenced: {ref_l}"
                    )

        # Load log paths
        ref_log_path = get_log_file(self.ref_nexus_file, "ref_nexus.log", self.tmp_path)
        gen_log_path = get_log_file(self.created_nexus, "gen_nexus.log", self.tmp_path)
        gen_lines, ref_lines = load_logs(gen_log_path, ref_log_path)

        # Compare logs
        compare_logs(gen_lines, ref_lines)
