import os
import logging
import numpy as np

from pynxtools.nexus.nexus import HandleNexus

# Set up the logger for the test output
logger = logging.getLogger("pynxtools")


def generate_ref_log():
    """
    Function to run the nexus test and generate the Ref_nexus_test.log file.
    """
    dirpath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../tests/data/nexus"
    )
    dirpath = os.path.abspath(dirpath)
    example_data = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../src/pynxtools/data/201805_WSe2_arpes.nxs",
    )
    example_data = os.path.abspath(example_data)

    # Ensure the directory exists for the log file
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    # Set up logger to write directly to the reference log
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    ref_log_path = os.path.join(dirpath, "Ref_nexus_test.log")
    handler = logging.FileHandler(ref_log_path, "w", encoding="utf-8")
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Set default print options for numpy (if needed)
    default_print_options = {
        "edgeitems": 3,
        "threshold": 1000,
        "precision": 8,
        "linewidth": 75,
    }

    np.set_printoptions(**default_print_options)

    # Run the actual processing with the nexus_helper
    nexus_helper = HandleNexus(logger, example_data, None, None)
    nexus_helper.process_nexus_master_file(None)

    print(f"Reference log generated at {ref_log_path}")


if __name__ == "__main__":
    generate_ref_log()
