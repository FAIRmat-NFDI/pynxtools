import logging
import os

try:
    from pynxtools.nomad.apis import DEFAULT_IMPORTS
    from pynxtools.nomad.apis.ontology import ensure_ontology_file
except ImportError as e:
    raise ImportError(
        "The 'pynxtools' package is required but not installed. "
        "Please install it before running this script."
    ) from e
logger = logging.getLogger("pynxtools")

ensure_ontology_file(DEFAULT_IMPORTS)