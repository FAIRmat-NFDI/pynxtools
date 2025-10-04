# Test functionality for `pynxtools` plugins

`pynxtools` contains a sub-module called `testing` which should be utilized to write automated tests for `pynxtools` reader plugins. This enables comprehensive tests of the plugin's functionality without needing detailed knowledge of the internal architecture of `pynxtools`, the technical details of the raw data files, or the plugin’s internal design.

!!! Note "Note"
    It is assumed that the plugin has the same structure internally as the [existing `pynxtools` plugins](../../reference/plugins.md).

## Why we need a test framework

To test integration of a plugin with the `pynxtools` core system, we need to:

1. Test the plugin's integration with `pynxtools` from the plugin's CI/CD.
2. Test in the `pynxtools` CI/CD if the plugin can be integrated with `pynxtools` properly.

## How to write an integration test for a reader plugin with `pynxtools.testing`

It is very simple to write a test to verify the plugin integration with `pynxtools` within the plugin's tests directory. The developer can place the test where they want, but they need to use the provided test interface from `pynxtools.testing`. An example test for a demo plugin `pynxtools-FOO` (which contains a reader called `foo` for an application definition `NXfoo`) is given below:

```python title="test_plugin.py"
import os

import pytest
from pynxtools.testing.nexus_conversion import ReaderTest

# e.g. module_dir = /pynxtools-foo/tests
module_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    "nxdl,reader_name,files_or_dir",
    [
        ("NXfoo", "foo", f"{module_dir}/../tests/data/test_data_dir_1"),
        ("NXfoo", "foo", f"{module_dir}/../tests/data/test_data_dir_2")
    ],
)
def test_foo_reader(nxdl, reader_name, files_or_dir, tmp_path, caplog):
    """Test for the FooReader or foo reader plugin.

    Parameters
    ----------
    nxdl : str
        Name of the NXDL application definition that is to be tested by
        this reader plugin (e.g. NXfoo), without the file ending .nxdl.xml.
    reader_name : str
        Name of the class of the reader (e.g. "foo")
    files_or_dir : class
        Name of the class of the reader.
    tmp_path : pytest.fixture
        Pytest fixture variable, used to create temporary file and clean up the generated files
        after test.
    caplog : pytest.fixture
        Pytest fixture variable, used to capture the log messages during the test.
    """
    # test plugin reader
    test = ReaderTest(nxdl, reader_name, files_or_dir, tmp_path, caplog)
    test.convert_to_nexus()
    # test.convert_to_nexus(caplog_level="ERROR", ignore_undocumented=True)
    # Use `ignore_undocumented` to skip undocumented fields
    # caplog_level can be "ERROR" or "WARNING"
    test.check_reproducibility_of_nexus()
    # Here, you can also pass `ignore_lines` (a list) or `ignore_sections` (a dict)
    # if you want to ignore certain lines or lines within a section in the comparison
    # of the log files of the reference -nxs file and the one created in the test.
```

The `ReaderTest.convert_to_nexus` method tries to convert all files in the `files_or_dir` directory to a NeXus file that is compliant with the application definition (`nxdl`), using a specific pynxtools reader (`reader_name`). In this example, the `foo` reader is used to convert to files following the `NXfoo` application definition.

There are some possibilities to configure this test for  your specific plugin:

- You can configure the test data that is used. Typically, this data should be located in `tests/data`, but it is also possible to use other data inside or even outside the test directory of the plugin.
- You can also pass additional parameters to `test.convert_to_nexus`:
  - `caplog_level` (str): This parameter determines the level at which the caplog is set during testing. This can be either "ERROR" (by default) or "WARNING". If it is "WARNING", the test will also fail if any warnings are reported by the reader.

  - `ignore_undocumented` (boolean): If true, the test skips the verification of undocumented keys. Otherwise, a warning message for undocumented keys is logged.

Afterwards, the `ReaderTest.convert_to_nexus` method uses the NeXus annotator tool [`read_nexus`](../../learn/pynxtools/nexus-validation.md#read_nexus-nexus-file-reader-and-debugger) (which is part of `pynxtools`) to create log files both of the reference NeXus file located in `files_or_dir` as well as the freshly created NeXus files. These log files are compared line-by-line to check that the created NeXus file is indeed the same as the reference file.

This test can also be configured:

- You can pass a keyword argument `ignore_lines` to `check_reproducibility_of_nexus`. `ignore_lines` is expected to be a list of lines for which the comparison shall be skipped. Specifically, any line that starts with any of the strings in `ignore_lines` is ignored.
- In adddition, you can disable the comparison for a given line for a NeXus concept in the `read_nexus` output using the `ignore_sections` keyword. As an example, a typical section for a NeXus field in the output looks like this:

    ```
    DEBUG: 
    ===== FIELD (//entry/start_time): <HDF5 dataset "start_time": shape (), type "|O">
    DEBUG: ===== FIELD (//entry/start_time): <HDF5 dataset "start_time": shape (), type "|O">
    value: 2018-05-01T07:22:00+02:00 
    DEBUG: value: 2018-05-01T07:22:00+02:00 
    classpath: ['NXentry', 'NX_DATE_TIME']
    DEBUG: classpath: ['NXentry', 'NX_DATE_TIME']
    classes:
    NXarpes.nxdl.xml:/ENTRY/start_time
    NXentry.nxdl.xml:/start_time
    DEBUG: classes:
    NXarpes.nxdl.xml:/ENTRY/start_time
    NXentry.nxdl.xml:/start_time
    <<REQUIRED>>
    DEBUG: <<REQUIRED>>
    documentation (NXarpes.nxdl.xml:/ENTRY/start_time):
    DEBUG: documentation (NXarpes.nxdl.xml:/ENTRY/start_time):
    ```

    If you do want to disable the comparison for the value of `entry/start_time`, you can pass a dictionary to `ignore_sections`. In this example, the dictionary `{"FIELD (//entry/start_time)": ["value:"]}` would disable the comparison of the `value` line. Any other line in this section can be disabled by adding more strings to the list (e.g. `DEBUG - value:`), whereas additional sections can be ignored by adding to the `ignore_sections` dictionary.

## How to write an integration test for a NOMAD example in a reader plugin

It is also possible to ship NOMAD Example Uploads directly with the reader plugin. As an example, `pynxtools-mpes` comes with its own [NOMAD examplehere](https://github.com/FAIRmat-NFDI/pynxtools-mpes/tree/bring-in-examples/src/pynxtools_mpes/nomad) using the [`ExampleUploadEntryPoint`](https://nomad-lab.eu/prod/v1/staging/docs/howto/plugins/example_uploads.html) of NOMAD.

The `testing` sub-package of `pynxtools` provides two functionalities for testing the `ExampleUploadEntryPoint` defined in a `pynxtools` plugin:

1. Test that the `ExampleUploadEntryPoint` instance can be properly loaded.
2. Test that the schemas and files in the example folder(s) can be parsed by NOMAD.

We will write a test for a `pynxtools_foo_example_entrypoint` defined in the pyproject.toml file of a demo `pynxtools-FOO` repository. Here the actual example data resides in the folder `src/pynxtools_foo/nomad/examples` and the plugin package is called `pynxtools_foo`:

```python title="pyproject.toml"
[project.entry-points.'nomad.plugin']
pynxtools_foo_example = "pynxtools_foo.nomad.entrypoints:pynxtools_foo_example_entrypoint"
```

```python title="src/pynxtools_foo/nomad/nomad_example_entrypoint.py"
from nomad.config.models.plugins import ExampleUploadEntryPoint

pynxtools_foo_example_entrypoint = ExampleUploadEntryPoint(
    title="My example upload",
    description="This is an example upload for the pynxtools-FOO package.",
    plugin_package="pynxtools_foo",
    resources=["nomad/examples/*"],
)
```

A test for the `pynxtools_foo_example_entrypoint` could look like this:

```python title="test_nomad_examples.py"
import nomad

from pynxtools.testing.nomad_example import (
    get_file_parameter,
    parse_nomad_examples,
    example_upload_entry_point_valid,
)

from pynxtools_foo.nomad.entrypoints import pynxtools_foo_example_entrypoint

EXAMPLE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "src",
    "pynxtools_foo",
    "nomad",
    "examples",
)

@pytest.mark.parametrize(
    "mainfile",
    get_file_parameter(EXAMPLE_PATH),
)
def test_parse_nomad_examples(mainfile):
    """Test if NOMAD examples work."""
    archive_dict = parse_nomad_examples(mainfile)
    # Here, you can also implement more logic if you know the contents of the `archive_dict`.


@pytest.mark.parametrize(
    ("entrypoint", "example_path"),
    [
        pytest.param(
            pynxtools_foo_example_entrypoint,
            EXAMPLE_PATH,
            id="pynxtools_foo_example",
        ),
    ],
)
def test_example_upload_entry_point_valid(entrypoint, example_path):
    """Test if NOMAD ExampleUploadEntryPoint works."""
    example_upload_entry_point_valid(
        entrypoint=entrypoint,
        example_path=example_path,
    )

```
