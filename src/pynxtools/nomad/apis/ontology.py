import logging
import os
import subprocess
from pathlib import Path

import pygit2
import structlog

os.environ["OWLREADY2_JAVA_LOG_LEVEL"] = "WARNING"

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from nomad.config import config
from owlready2 import ThingClass, get_ontology, sync_reasoner
from owlready2.namespace import Ontology

from pynxtools.NeXusOntology.script.generate_ontology import main as generate_ontology
from pynxtools.nomad.utils import CACHE_DIR, NOMAD_PACKAGE_DIR, resolve_artifact_path

logger = logging.getLogger("pynxtools")


def get_ontology_filepath(owl_filename: str) -> Path:
    local_ontology_dir = NOMAD_PACKAGE_DIR.parent / "NeXusOntology" / "ontology"

    return resolve_artifact_path(
        filename=owl_filename,
        package_dir=local_ontology_dir,
        cache_dir=CACHE_DIR,
    )


INFERRED_OWL_FILE_PATH = None


def ensure_ontology_file(imports: list[str] | None = None):
    """
    Verify that a inferred ontology file matching the latest definitions exists.
    If it is missing, regenerate the ontology, run the reasoner, and save the inferred ontology.
    """
    if imports is None:
        imports = []

    global INFERRED_OWL_FILE_PATH

    try:
        # Get the latest commit hash from the definitions submodule in pynxtools
        nexus_def_path = str(NOMAD_PACKAGE_DIR.parent / "definitions")
        repo = pygit2.Repository(nexus_def_path)
        latest_commit_hash = str(repo.head.target)[:7]

        # Construct the expected ontology file paths
        full_owl_file_path = get_ontology_filepath(
            f"NeXusOntology_full_{latest_commit_hash}.owl"
        )
        inferred_owl_file_path = get_ontology_filepath(
            f"NeXusOntology_full_{latest_commit_hash}_inferred.owl"
        )

        # Ensure the parent path exists if we are using the cache
        if inferred_owl_file_path.parent.is_relative_to(CACHE_DIR):
            inferred_owl_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Check if the inferred ontology file exists, if not, generate it
        if not inferred_owl_file_path.is_file():
            generate_ontology(
                full=True,
                testdata=False,
                nexus_def_path=nexus_def_path,
                def_commit=latest_commit_hash,
                store_commit_filename=True,
                imports=imports,
                output_dir=str(full_owl_file_path.parent),
            )
            if full_owl_file_path.is_file():
                # Run reasoner and replace the ontology file with its inferred version
                ontology = get_ontology(str(full_owl_file_path)).load()
                sync_reasoner(ontology)
                ontology.save(file=str(inferred_owl_file_path), format="rdfxml")
                full_owl_file_path.unlink()  # Remove the non-inferred file

        # Update the OWL_FILE_PATH to point to the inferred ontology file
        INFERRED_OWL_FILE_PATH = inferred_owl_file_path

    except Exception as e:
        raise RuntimeError(f"Failed to ensure ontology file: {e}")


def load_ontology() -> Ontology:
    try:
        ensure_ontology_file()
        if not INFERRED_OWL_FILE_PATH:
            raise RuntimeError("OWL_FILE_PATH is not set")

        if INFERRED_OWL_FILE_PATH.is_file():
            # load the preexisting inferred ontology
            ontology = get_ontology(str(INFERRED_OWL_FILE_PATH)).load()
            return ontology
        else:
            raise FileNotFoundError(
                f"Ontology file not found at {INFERRED_OWL_FILE_PATH}"
            )
    except Exception as e:
        logger.error(f"Error loading ontology: {e}", exc_info=True)
        raise


def get_label(entity):
    # Try to get rdfs:label, else fallback to name or IRI
    if hasattr(entity, "label") and entity.label:
        return entity.label[0]
    elif hasattr(entity, "name"):
        return entity.name
    else:
        return str(entity)


def format_nxclass_label(nxclass):
    label = get_label(nxclass)
    iri = getattr(nxclass, "iri", None)
    if iri and "PaNET" in iri:
        code = iri.split("/")[-1]
        return f"{label} ({code})"
    elif iri and "nexusformat" in iri:
        return f"{label}"
    elif iri:
        return f"{label} ({iri})"
    else:
        return f"{label}"


def fetch_superclasses(ontology, class_name):
    try:
        cls = ontology.search_one(iri="*" + class_name)
        if cls is None:
            raise ValueError(f"Class '{class_name}' not found in the ontology.")
        candidates = cls.ancestors()

        # Exclude NeXusApplicationClass and its superclasses
        nexus_application_class = ontology.search_one(iri="*NeXusApplicationClass")
        unwanted_superclasses = set()
        if nexus_application_class is not None:
            unwanted_superclasses |= {
                sc.iri
                for sc in nexus_application_class.ancestors()
                if hasattr(sc, "iri")
            }
            unwanted_superclasses.add(nexus_application_class.iri)

        # Exclude PaNET00001 to PaNET00005 and their superclasses
        for panet_code in range(1, 6):
            panet_iri = f"http://purl.org/pan-science/PaNET/PaNET{panet_code:05d}"
            panet_class = ontology.search_one(iri=panet_iri)
            if panet_class is not None:
                unwanted_superclasses |= {
                    sc.iri for sc in panet_class.ancestors() if hasattr(sc, "iri")
                }
                unwanted_superclasses.add(panet_class.iri)

        direct_superclasses = [
            sc
            for sc in candidates
            if hasattr(sc, "iri")
            and sc.iri not in unwanted_superclasses
            and (
                ("PaNET" in sc.iri) or ("nexusformat" in sc.iri) or ("ESRFET" in sc.iri)
            )
            and isinstance(sc, ThingClass)
        ]
        return [format_nxclass_label(sc) for sc in direct_superclasses]
    except Exception as e:
        logger.error(f"Error in fetch_superclasses: {e}")
        raise
