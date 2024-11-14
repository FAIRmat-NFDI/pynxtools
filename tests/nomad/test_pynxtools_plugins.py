import os
import subprocess
import pytest


@pytest.mark.parametrize(
    "plugin_name",
    [
        # pytest.param("pynxtools-apm"),
        # pytest.param("pynxtools-ellips"),
        # pytest.param("pynxtools-em"),
        pytest.param("pynxtools-mpes"),
        # pytes.param("pynxtools-raman"),
        # pytes.param("pynxtools-stm"),
        # pytest.param("pynxtools-xps"),
        # pytest.param("pynxtools-xrd"),
    ],
)
def test_plugins(plugin_name):
    """
    Test the execution of plugin tests for each given plugin. This simulates
    the environment where the IN_NOMAD_DISTRO environment variable is set to "true". In this
    mode, only tests in the "tests/nomad" directory are executed for the selected plugin.

    The function performs the following steps:
    1. Sets the IN_NOMAD_DISTRO environment variable to "true" to simulate the desired environment.
    2. Executes the `plugin_test.py` script using the subprocess module, passing the plugin name
       through the `--plugin` flag to run tests for the specified plugin.
    3. Asserts that the subprocess completes successfully (i.e., the return code is 0).
    4. Captures the output from the subprocess and checks that there are no errors in the

    """
    # Set the IN_NOMAD_DISTRO environment variable to True for sweep
    os.environ["IN_NOMAD_DISTRO"] = "true"

    # Run the main plugin_test.py script with the --sweep argument
    result = subprocess.run(
        ["python", "scripts/plugin_test.py", "--plugin", plugin_name],
        capture_output=True,
        text=True,
        check=False,
    )

    # Assert that the subprocess ran successfully
    assert result.returncode == 0, f"Tests failed. Output: {result.stderr}"
