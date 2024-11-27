import os
import subprocess
import sys
import argparse
import logging
from typing import List, Dict, Optional


# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

# Plugin configuration list with plugin details (name, branch, tests directory)
PLUGIN_CONFIGS: List[Dict[str, str]] = [
    {"plugin": "pynxtools-apm", "branch": "main", "tests_to_run": "tests/."},
    {"plugin": "pynxtools-ellips", "branch": "main", "tests_to_run": "tests/."},
    {"plugin": "pynxtools-em", "branch": "main", "tests_to_run": "tests/."},
    {"plugin": "pynxtools-raman", "branch": "main", "tests_to_run": "tests/."},
    {"plugin": "pynxtools-mpes", "branch": "main", "tests_to_run": "tests/."},
    {"plugin": "pynxtools-stm", "branch": "main", "tests_to_run": "tests/."},
    {"plugin": "pynxtools-xps", "branch": "main", "tests_to_run": "tests/."},
    {"plugin": "pynxtools-xrd", "branch": "main", "tests_to_run": "tests/."},
]


def get_tests_to_run(tests_to_run_default: str) -> str:
    """
    Determine which tests should be run based on the IN_NOMAD_DISTRO environment variable.

    If IN_NOMAD_DISTRO is set to "true", only tests in the "tests/nomad" directory will be run.
    Otherwise, the default test directory provided in the configuration is used.

    Args:
        tests_to_run_default (str): The default directory of tests to run if IN_NOMAD_DISTRO is not set to "true".

    Returns:
        str: The directory of tests to run.
    """
    if os.getenv("IN_NOMAD_DISTRO", "false").lower() == "true":
        return "tests/nomad"
    return tests_to_run_default


def run_command(
    command: List[str], cwd: Optional[str] = None
) -> Optional[subprocess.CompletedProcess]:
    """
    Run a command using subprocess and capture its output.

    Args:
        command (List[str]): The command to run, given as a list of arguments.
        cwd (Optional[str]): The directory in which to run the command. Defaults to None (current directory).

    Returns:
        Optional[subprocess.CompletedProcess]: The result of the subprocess run command.
    """
    try:
        result = subprocess.run(
            command, cwd=cwd, capture_output=True, text=True, check=False
        )

        if result.stdout:
            logger.info(result.stdout)
        if result.stderr:
            logger.error(result.stderr)

        return result
    except Exception as e:
        logger.error(f"Error running command {command}: {e}")
        return None


def clone_and_checkout(plugin: str, branch: str) -> None:
    """
    Clone a repository and checkout the specified branch.

    Args:
        plugin (str): The name of the plugin repository to clone.
        branch (str): The branch to checkout after cloning the repository.
    """
    logger.info(f"Setting up tests for {plugin} (branch: {branch})")
    clone_command = [
        "git",
        "clone",
        f"https://github.com/FAIRmat-NFDI/{plugin}.git",
        "--branch",
        branch,
        "--depth",
        "1",
    ]
    result = run_command(clone_command)

    if result is None or result.returncode != 0:
        logger.error(f"Failed to clone repository for '{plugin}' (branch '{branch}').")
        return

    logger.info(f"Repository cloned successfully for '{plugin}' (branch '{branch}').")


def install_local_plugin(plugin: str) -> None:
    """
    Install the plugin using pip.

    Args:
        plugin (str): The name of the plugin to install.
    """
    logger.info(f"Install local {plugin}")
    install_command = ["uv", "pip", "install", f"./{plugin}"]
    result = run_command(install_command)

    if result is None or result.returncode != 0:
        logger.error(f"Failed to install repository '{plugin}'.")
        return

    logger.info(f"Repository installed successfully for '{plugin}'.")


def run_tests(plugin: str, tests_to_run: str) -> None:
    """
    Run the tests for a specified plugin.

    Args:
        plugin (str): The plugin for which to run tests.
        tests_to_run (str): The directory containing the tests to run.
    """
    pytest_command = ["pytest", f"./{plugin}/{tests_to_run}"]

    result = run_command(pytest_command)

    if result is None or result.returncode != 0:
        logger.error(f"Error running tests for {plugin}: {plugin}")
        sys.exit(1)

    logger.info(f"Successfully ran tests for '{plugin}'.")


if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Run plugin tests.")
    parser.add_argument("--plugin", help="Specific plugin to test")

    args = parser.parse_args()

    # Determine which plugins to test based on the arguments passed
    if args.plugin:
        plugins_to_test = [
            cfg for cfg in PLUGIN_CONFIGS if cfg["plugin"] == args.plugin
        ]
    else:
        plugins_to_test = (
            PLUGIN_CONFIGS  # Run all plugins if no specific plugin is provided
        )

    # If no plugins are specified, exit with an error
    if not plugins_to_test:
        logger.error("No plugins specified or found for testing.")
        sys.exit(1)

    # Iterate through the selected plugins and run the tests
    for config in plugins_to_test:
        plugin, branch, tests_to_run_default = (
            config["plugin"],
            config["branch"],
            config["tests_to_run"],
        )
        tests_to_run = get_tests_to_run(tests_to_run_default=tests_to_run_default)
        # Clone the repository, checkout the branch, and
        clone_and_checkout(plugin, branch)

        # If IN_NOMAD_DISTRO is false, install the plugin locally
        if os.getenv("IN_NOMAD_DISTRO", "false").lower() == "false":
            install_local_plugin(plugin)

        # run the plugin's tests
        run_tests(plugin, tests_to_run)
