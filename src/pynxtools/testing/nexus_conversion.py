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
from typing import Literal, Optional

import structlog

try:
    from nomad.client import parse

    NOMAD_AVAILABLE = True
except ImportError:
    NOMAD_AVAILABLE = False


from pynxtools.annotator.annotator import Annotator
from pynxtools.dataconverter.convert import convert, get_reader
from pynxtools.dataconverter.helpers import (
    add_default_root_attributes,
    get_nxdl_root_and_path,
)
from pynxtools.dataconverter.validate_file import validate
from pynxtools.nexus.handler import NexusFileHandler


def get_log_file(nxs_file, log_file, tmp_path):
    """Get log file for the nexus file with read_nexus tools."""
    logger = logging.getLogger(__file__)
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    log_file = os.path.join(tmp_path, log_file)
    handler = logging.FileHandler(log_file, "w")
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    NexusFileHandler(nxs_file).process(Annotator(logger))

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
        kwargs : dict[str, Any]
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
        assert hasattr(self.reader, "supported_nxdls"), (
            f"Reader{self.reader} must have supported_nxdls attribute"
        )
        assert callable(self.reader.read), f"Reader{self.reader} must have read method"

        if isinstance(self.files_or_dir, list | tuple):
            example_files = self.files_or_dir
        else:
            example_files = sorted(glob(os.path.join(self.files_or_dir, "*")))
        self.ref_nexus_file = [file for file in example_files if file.endswith(".nxs")][
            0
        ]
        input_files = [
            file
            for file in example_files
            if not file.endswith((".nxs", "ref_output.txt"))
        ]
        assert self.ref_nexus_file, "Reference nexus (.nxs) file not found"

        assert (
            self.nxdl in self.reader.supported_nxdls
            or "*" in self.reader.supported_nxdls
        ), f"Reader does not support {self.nxdl} NXDL."

        nxdl_root, nxdl_file = get_nxdl_root_and_path(self.nxdl)
        assert os.path.exists(nxdl_file), f"NXDL file {nxdl_file} not found"

        # Clear the log of `convert`
        self.caplog.clear()

        with self.caplog.at_level(caplog_level):
            _ = convert(
                input_file=tuple(input_files),
                reader=self.reader_name,
                nxdl=self.nxdl,
                skip_verify=False,
                ignore_undocumented=ignore_undocumented,
                output=self.created_nexus,
                **self.kwargs,
            )

        test_output = self.caplog.messages

        files_with_expected_output = [
            file for file in example_files if file.endswith("ref_output.txt")
        ]

        if files_with_expected_output:
            output_file = files_with_expected_output[0]
            with open(output_file) as file:
                expected_messages = [line.strip() for line in file.readlines()]

            for message in expected_messages:
                if caplog_level == "WARNING":
                    if message.startswith(("WARNING", "ERROR")):
                        test_output.remove(message)
                if caplog_level == "ERROR":
                    if message.startswith("ERROR"):
                        test_output.remove(message)

        assert test_output == []

        # Validate created file using the validate_nexus functionality
        with self.caplog.at_level(caplog_level):
            validate(self.created_nexus, ignore_undocumented=ignore_undocumented)

        if NOMAD_AVAILABLE:
            kwargs = dict(
                strict=True,
                parser_name=None,
                server_context=False,
                username=None,
                password=None,
            )

            # Set level of all structlog loggers to "INFO"
            structlog.configure(
                wrapper_class=structlog.make_filtering_bound_logger(logging.INFO)
            )
            parse(self.created_nexus, **kwargs)

    def check_reproducibility_of_nexus(self, **kwargs):
        """Reproducibility test for the generated nexus file.

        Compares the annotator log produced from the generated NeXus file against
        the log from the reference file, ignoring lines that are expected to differ
        between runs (file paths, timestamps, library versions).

        Keyword Args
        ------------
        ignore_lines : list[str]
            Additional line prefixes to ignore.  Each pattern is matched against
            the *stripped* line, so indentation does not need to be included.
            Use this to suppress reader-specific entries that always differ
            (e.g. ``["@creator_version"]``).
        ignore_sections : dict[str, list[str]]
            Section-specific line prefixes to ignore.  A new section begins
            whenever a stripped log line starts with ``"FIELD "`` or ``"GROUP "``.
            Keys are matched via ``startswith`` against the stripped section-header
            line; values are additional ignore prefixes applied to subsequent lines
            within that section.

            Example — ignore the ``Value`` detail line for a specific field::

                ignore_sections = {
                    "FIELD /Ag__002__VB/start_time ": ["Value"],
                }

            A trailing space in the key is useful to avoid matching longer paths
            that share the same prefix (the header line continues with
            ``shape=... dtype=...`` after a space).
        """
        reader_ignore_lines: list[str] = kwargs.get("ignore_lines", [])
        reader_ignore_sections: dict[str, list[str]] = kwargs.get("ignore_sections", {})

        # Lines whose stripped form starts with any of these prefixes are ignored.
        # Only entries that are *structurally guaranteed* to differ between any
        # generated file and any reference file belong here.  Environment-specific
        # differences (library versions, definitions commit hashes, pynxtools version)
        # must be added by each plugin via the ``ignore_lines`` parameter.
        IGNORE_LINES: list[str] = reader_ignore_lines + [
            "NeXus file",  # file path: gen goes to tmp_path, ref is committed
            "@NeXus_release",  # differs due to submodule checkout in tests
            "@NeXus_repository",  # differs due to submodule checkout in tests
            "@file_name",  # original filename: <filename>.nxs vs ref name
            "@file_time",  # creation timestamp: always differs
            "@file_update_time",  # update timestamp: always differs
            "@creator_version",  # differs due to checkout in tests
        ]

        IGNORE_SECTIONS: dict[str, list[str]] = {
            **reader_ignore_sections,
            "ATTRS (//@HDF5_Version)": ["DEBUG - value:"],
            "ATTRS (//@file_name)": ["DEBUG - value:"],
            "ATTRS (//@file_time)": ["DEBUG - value:"],
            "ATTRS (//@file_update_time)": ["DEBUG - value:"],
            "ATTRS (//@h5py_version)": ["DEBUG - value:"],
        }

        # Section headers: a stripped line starting with one of these prefixes
        # begins a new section; section-specific ignores then apply until the next.
        _SECTION_PREFIXES = ("FIELD ", "GROUP ")
        IGNORE_SECTIONS: dict[str, list[str]] = reader_ignore_sections

        def get_section_ignores(stripped_line: str) -> list[str]:
            """Return section-specific ignore prefixes for the given header line."""
            for key, patterns in IGNORE_SECTIONS.items():
                if stripped_line.startswith(key):
                    return patterns
            return []

        def should_skip_line(*lines: str, ignore_lines: list[str]) -> bool:
            """Return True if all lines match any ignored prefix (after stripping)."""
            return any(
                all(line.strip().startswith(ignore) for line in lines)
                for ignore in ignore_lines
            )

        def load_logs(
            gen_log_path: str, ref_log_path: str
        ) -> tuple[list[str], list[str]]:
            """Load log files and return their contents as lists of lines."""
            with (
                open(gen_log_path, encoding="utf-8") as gen,
                open(ref_log_path, encoding="utf-8") as ref,
            ):
                return gen.readlines(), ref.readlines()

        def compare_logs(gen_lines: list[str], ref_lines: list[str]) -> None:
            """Compare log lines, ignoring lines listed in IGNORE_LINES."""

            def extra_lines(lines1: list[str], lines2: list[str]) -> list[str]:
                """Return lines present in lines1 but absent in lines2 (non-ignored)."""
                diffs: list[str] = []
                section_ignores: list[str] = []
                for ind, line in enumerate(lines1):
                    stripped = line.strip()
                    if any(stripped.startswith(p) for p in _SECTION_PREFIXES):
                        section_ignores = get_section_ignores(stripped)
                    if line not in lines2 and not should_skip_line(
                        line, ignore_lines=IGNORE_LINES + section_ignores
                    ):
                        diffs.append(f"{stripped} (line: {ind})")
                return diffs

            # Case 1: line counts differ
            if len(gen_lines) != len(ref_lines):
                diffs_gen = extra_lines(gen_lines, ref_lines)
                diffs_ref = extra_lines(ref_lines, gen_lines)

                error_msg = (
                    f"Log files are different: mismatched line counts. "
                    f"Generated file has {len(gen_lines)} lines, "
                    f"while reference file has {len(ref_lines)} lines."
                )
                if diffs_gen:
                    error_msg += "\n\nExtra lines in generated:\n" + "\n".join(
                        diffs_gen
                    )
                if diffs_ref:
                    error_msg += "\n\nExtra lines in reference:\n" + "\n".join(
                        diffs_ref
                    )

                raise AssertionError(error_msg)

            # Case 2: same line counts, check for diffs line by line
            diffs: list[str] = []
            section_ignores: list[str] = []
            for ind, (gen_l, ref_l) in enumerate(zip(gen_lines, ref_lines)):
                gen_stripped = gen_l.strip()
                if any(gen_stripped.startswith(p) for p in _SECTION_PREFIXES):
                    section_ignores = get_section_ignores(gen_stripped)
                if gen_l != ref_l and not should_skip_line(
                    gen_l, ref_l, ignore_lines=IGNORE_LINES + section_ignores
                ):
                    diffs.append(
                        f"Log files are different at line {ind}:\n"
                        f"  generated: {gen_l}  reference: {ref_l}"
                    )
            if diffs:
                raise AssertionError("\n".join(diffs))

        # Load log paths
        ref_log_path = get_log_file(self.ref_nexus_file, "ref_nexus.log", self.tmp_path)
        gen_log_path = get_log_file(self.created_nexus, "gen_nexus.log", self.tmp_path)
        gen_lines, ref_lines = load_logs(gen_log_path, ref_log_path)

        # Compare logs
        compare_logs(gen_lines, ref_lines)
