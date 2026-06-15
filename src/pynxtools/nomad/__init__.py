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
import os
from pathlib import Path
from typing import Optional

import numpy as np

from pynxtools import get_nexus_version

try:
    from nomad import config
    from nomad.metainfo.data_type import (
        Bytes,
        Datetime,
        m_bool,
        m_complex128,
        m_float64,
        m_int,
        m_int64,
        m_str,
    )
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

REPLACEMENT_FOR_NX = ""

# This is a list of NeXus group names that are not allowed because they are defined as quantities in the BaseSection class.
UNALLOWED_GROUP_NAMES = {"name", "datetime", "lab_id", "description"}

NX_TYPES = {  # Primitive Types,  'ISO8601' is the only type not defined here
    "NX_COMPLEX": m_complex128,
    "NX_FLOAT": m_float64,
    "NX_CHAR": m_str,
    "NX_BOOLEAN": m_bool,
    "NX_INT": m_int64,
    "NX_UINT": m_int64,
    "NX_NUMBER": m_float64,
    "NX_POSINT": m_int64,
    "NX_BINARY": Bytes,
    "NX_DATE_TIME": Datetime,
    "NX_CHAR_OR_NUMBER": m_float64,  # TODO: fix this mapping
}


FIELD_STATISTICS: dict[str, dict] = {
    "__mean": {"function": np.mean, "type": np.float64, "mask": True},
    # "__std": {"function": np.std, "type": np.float64, "mask": True},
    "__min": {"function": np.min, "type": None, "mask": True},
    "__max": {"function": np.max, "type": None, "mask": True},
    "__size": {
        "function": np.size,
        "type": np.int64,
        "mask": False,
    },  # old value np.int32 could have overflown if array values are larger than 2**32
    "__ndim": {
        "function": np.ndim,
        "type": np.uint8,
        "mask": False,
    },  # old value np.int32 unnecessarily exceeds max ndims in HDF5 which is 32
}


def _rename_classes_in_nomad(nx_name: str) -> str:
    """
    Modify group names that conflict with NOMAD due to being defined as quantities
    in the BaseSection class by appending '__group' to those names.

    Some quantities names names are reserved in the BaseSection class (or even higher up in metainfo),
    and thus require renaming to avoid collisions.

    Args:
        nx_name (str): The original group name.

    Returns:
        Optional[str]: The modified group name with '__group' appended if it's in
        UNALLOWED_GROUP_NAMES, or the original name if no change is needed.
    """
    return nx_name + "__group" if nx_name in UNALLOWED_GROUP_NAMES else nx_name


def _rename_nx_for_nomad(
    name: str,
    is_group: bool = False,
    is_field: bool = False,
    is_attribute: bool = False,
) -> str | None:
    """
    Rename NXDL names for compatibility with NOMAD, applying specific rules
    based on the type of the NeXus concept. (group, field, or attribute).

    - NXobject is unchanged.
    - NX-prefixed names (e.g., NXdata) are renamed by replacing 'NX' with a custom string.
    - Group names are passed to _rename_classes_in_nomad(), and the result is capitalized.
    - Fields and attributes have '__field' or '__attribute' appended, respectively.

    Args:
        name (str): The NXDL name.
        is_group (bool): Whether the name represents a group.
        is_field (bool): Whether the name represents a field.
        is_attribute (bool): Whether the name represents an attribute.

    Returns:
        Optional[str]: The renamed NXDL name, with group names capitalized,
        or None if input is invalid.
    """
    if name and name.startswith("NX"):
        name = REPLACEMENT_FOR_NX + name[2:]
        name = name[0].upper() + name[1:]

    if name[0] in "0123456789":
        name = f"_{name}"

    if is_group:
        name = _rename_classes_in_nomad(name)
    elif is_field:
        name += "__field"
    elif is_attribute:
        pass
    return name


def get_quantity_base_name(quantity_name):
    return (
        quantity_name[:-7]
        if quantity_name.endswith("__field") and quantity_name[-8] != "_"
        else quantity_name
    )


PACKAGE_DIR = Path(__file__).resolve().parent
CACHE_DIR = Path(config.fs.tmp) / "pynxtools"


def resolve_artifact_path(
    *,
    filename: str,
    package_dir: Path,
    cache_dir: Path,
    build_env_var: str = "PYNXTOOLS_BUILD_PACKAGE",
) -> Path:
    """Resolve the path for a generated artifact.

    Resolution order:

    1. If ``build_env_var`` is ``"1"``, always return the path inside
       ``PACKAGE_DIR`` (ensures inclusion in built distributions).
    2. If the file exists in ``PACKAGE_DIR``, return that path.
    3. Otherwise, return the corresponding path inside ``CACHE_DIR`` for
       development or first-time generation.

    This function does not generate the file.

    Returns:
        Path: Resolved location for reading or writing the JSON file.
    """
    # 1. Build-mode override (forces packaging the file)
    if os.environ.get(build_env_var) == "1":
        return package_dir

    # 2. Use packaged file if it exists
    packaged = package_dir / filename
    if packaged.exists():
        return packaged

    # 3. Otherwise store in cache dir
    # create parent directory only if we need to write
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / filename


def get_package_filepath() -> Path:
    filename = f"nxs_metainfo_package_{get_nexus_version()}.json"

    return resolve_artifact_path(
        filename=filename,
        package_dir=PACKAGE_DIR / "schema_packages",
        cache_dir=CACHE_DIR,
    )

def ensure_ontology_initialization() -> None:
    """
    Ensure the NeXus ontology file exists at the expected location for nomad-ontology-service.
    
    The ontology service expects: {config.fs.tmp}/pynxtools/NeXusOntology_inferred.owl
    This function ensures the file is generated and available at that location.
    Should be called during schema initialization.
    
    Uses a lock file to prevent concurrent generation in multi-process environments.
    """
    import logging
    import shutil
    import time
    from pathlib import Path
    
    try:
        import pygit2
        from owlready2 import get_ontology, sync_reasoner
        from pynxtools.NeXusOntology.script.generate_ontology import main as generate_ontology
        
        logger = logging.getLogger("pynxtools")
        
        # Ensure cache dir is absolute
        cache_dir_abs = CACHE_DIR.resolve()
        
        # Expected path for the service
        expected_ontology_path = cache_dir_abs / "NeXusOntology_inferred.owl"
        
        # Lock file to prevent concurrent generation
        lock_file = cache_dir_abs / ".ontology_generation.lock"
        
        # If file already exists and is valid, we're done
        if expected_ontology_path.is_file():
            logger.debug(f"Ontology file exists at {expected_ontology_path}")
            return
        
        # Ensure cache directory exists
        cache_dir_abs.mkdir(parents=True, exist_ok=True)
        
        # Check if another process is generating (lock file exists)
        if lock_file.exists():
            logger.info("Ontology generation in progress by another process, waiting...")
            # Wait up to 120 seconds for the other process to complete
            for attempt in range(120):
                time.sleep(1)
                if expected_ontology_path.is_file():
                    logger.debug("Ontology file ready (generated by another process)")
                    return
                if not lock_file.exists():
                    logger.debug("Lock released, checking if file was generated...")
                    if expected_ontology_path.is_file():
                        return
                    break
            logger.warning("Timeout waiting for ontology generation, will retry...")
        
        # Acquire lock
        try:
            lock_file.touch(exist_ok=False)
        except FileExistsError:
            # Another process just grabbed it, wait a bit
            time.sleep(2)
            if expected_ontology_path.is_file():
                return
            logger.warning("Could not acquire lock, proceeding anyway...")
            return
        
        try:
            logger.info("Initializing NeXus ontology for ontology service...")
            
            # Get imports from plugin config if available
            ontology_imports = []
            try:
                ep = config.get_plugin_entry_point("nomad_ontology_service:ontology_service")
                if ep and hasattr(ep, 'ontologies') and ep.ontologies:
                    # TODO: support selecting the correct ontology if multiple are defined
                    ontology_imports = ep.ontologies[0].imports
                    logger.info(f"Using ontology imports from config: {ontology_imports}")
            except Exception:
                pass

            # Get latest commit hash from definitions
            nexus_def_path = str(PACKAGE_DIR.parent / "definitions")
            repo = pygit2.Repository(nexus_def_path)
            latest_commit_hash = str(repo.head.target)[:7]
            
            # Paths for versioned files
            full_owl_path = cache_dir_abs / f"NeXusOntology_full_{latest_commit_hash}.owl"
            inferred_owl_path = cache_dir_abs / f"NeXusOntology_full_{latest_commit_hash}_inferred.owl"
            
            # Generate if needed
            if not inferred_owl_path.is_file():
                logger.info(f"Generating ontology at {inferred_owl_path}")
                logger.info(f"Using imports: {ontology_imports}")
                generate_ontology(
                    full=True,
                    testdata=False,
                    nexus_def_path=nexus_def_path,
                    def_commit=latest_commit_hash,
                    store_commit_filename=True,
                    imports=ontology_imports,
                    output_dir=str(cache_dir_abs),
                )
                
                # Run reasoner if full ontology was created
                if full_owl_path.is_file():
                    logger.info("Running reasoner on full ontology...")
                    try:
                        # Pre-load imports into the world to ensure the reasoner sees them
                        for imp_iri in ontology_imports:
                            try:
                                logger.debug(f"Pre-loading import for reasoner: {imp_iri}")
                                get_ontology(imp_iri).load()
                            except Exception as e:
                                logger.warning(f"Could not load import {imp_iri}: {e}")

                        ontology = get_ontology(str(full_owl_path)).load()
                        sync_reasoner(ontology)
                        ontology.save(file=str(inferred_owl_path), format="rdfxml")
                        logger.info(f"Inferred ontology saved to {inferred_owl_path}")
                        # Remove the non-inferred version
                        if full_owl_path.exists():
                            full_owl_path.unlink()
                    except Exception as e:
                        logger.warning(f"Failed to run reasoner: {e}. Using non-inferred ontology.")
                        # Fall back to using the full ontology if reasoner fails
                        if not inferred_owl_path.is_file() and full_owl_path.is_file():
                            shutil.copy2(full_owl_path, inferred_owl_path)
            
            # Link/copy to expected path (handle existing files/symlinks)
            if inferred_owl_path.is_file():
                if expected_ontology_path.is_symlink() or expected_ontology_path.exists():
                    # Remove existing symlink or file
                    expected_ontology_path.unlink()
                
                logger.info(f"Creating link to {expected_ontology_path}")
                try:
                    expected_ontology_path.symlink_to(inferred_owl_path.name)
                except (OSError, NotImplementedError):
                    logger.info("Symlink not supported, copying file instead")
                    shutil.copy2(inferred_owl_path, expected_ontology_path)
            
            if expected_ontology_path.is_file():
                logger.info(f"Ontology ready at {expected_ontology_path}")
            else:
                logger.warning(f"Ontology file not found at {expected_ontology_path}")
        
        finally:
            # Always release the lock
            if lock_file.exists():
                lock_file.unlink()
        
    except Exception as e:
        logger.error(f"Failed to initialize ontology: {e}", exc_info=True)
        # Don't raise - ontology service will handle missing files gracefully