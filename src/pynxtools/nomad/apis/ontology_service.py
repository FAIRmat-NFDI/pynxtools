######################################################################
######################## import libraries ############################
######################################################################
import logging
import os
import subprocess

import pygit2

os.environ["OWLREADY2_JAVA_LOG_LEVEL"] = "WARNING"

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from nomad.config import config
from owlready2 import ThingClass, get_ontology, sync_reasoner
from owlready2.namespace import Ontology

from pynxtools.NeXusOntology.script.generate_ontology import main as generate_ontology

logger = logging.getLogger("pynxtools")

ontology_service_entry_point = config.get_plugin_entry_point(
    "pynxtools.nomad.apis:ontology_service"
)

#######################################################################
########################## define app and functions ###################
#######################################################################
app = FastAPI(
    root_path=f"{config.services.api_base_path}/ontology_service",
    title="Ontology Service",
    description="A service to provide ontological information for a given NeXus class.",
)

# Define local directory path and ontology directory path
local_dir = os.path.dirname(os.path.abspath(__file__))
ontology_dir = os.path.abspath(
    os.path.join(local_dir, "..", "..", "NeXusOntology", "ontology")
)
OWL_FILE_PATH = None


def ensure_ontology_file():
    """
    Verify that a inferred ontology file matching the latest definitions exists.
    If it is missing, regenerate the ontology, run the reasoner, and save the inferred ontology.
    """
    global OWL_FILE_PATH

    try:
        # Get the latest commit hash from the definitions submodule in pynxtools
        nexus_def_path = os.path.join(local_dir, "..", "..", "definitions")
        repo = pygit2.Repository(nexus_def_path)
        latest_commit_hash = str(repo.head.target)[:7]

        # Construct the expected inferred ontology file name and path
        inferred_owl_file_name = f"NeXusOntology_full_{latest_commit_hash}_inferred.owl"
        inferred_owl_file_path = os.path.join(ontology_dir, inferred_owl_file_name)
        # Check if the inferred ontology file exists, if not, generate it
        if not os.path.exists(inferred_owl_file_path):
            generate_ontology(
                full=True,
                testdata=False,
                nexus_def_path=nexus_def_path,
                def_commit=latest_commit_hash,
                store_commit_filename=True,
                imports=[
                    "https://raw.githubusercontent.com/pan-ontologies/esrf-ontologies/refs/heads/oscars-deliverable-2/ontologies/esrfet/ESRFET.owl"
                ],
            )
            # construct the path to the ontology file just generated
            owl_file_path = os.path.join(
                ontology_dir, f"NeXusOntology_full_{latest_commit_hash}.owl"
            )
            if os.path.exists(owl_file_path):
                # Run reasoner and replace the ontology file with its inferred version
                ontology = get_ontology(owl_file_path).load()
                sync_reasoner(ontology)
                ontology.save(file=inferred_owl_file_path, format="rdfxml")
                os.remove(owl_file_path)  # Remove the non-inferred file

        # Update the OWL_FILE_PATH to point to the inferred ontology file
        OWL_FILE_PATH = inferred_owl_file_path

    except Exception as e:
        raise RuntimeError(f"Failed to ensure ontology file: {e}")


def load_ontology() -> Ontology:
    try:
        ensure_ontology_file()
        if not OWL_FILE_PATH:
            raise RuntimeError("OWL_FILE_PATH is not set")

        if os.path.exists(OWL_FILE_PATH):
            # load the preexisting inferred ontology
            ontology = get_ontology(OWL_FILE_PATH).load()
            return ontology
        else:
            raise FileNotFoundError(f"Ontology file not found at {OWL_FILE_PATH}")
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


#######################################################################
########################## application routes #########################
#######################################################################
@app.on_event("startup")
def startup_event():
    """
    Ensure the ontology file is present during application startup.
    if not, generate it.
    """
    try:
        ensure_ontology_file()
    except Exception as e:
        logger.error(f"Error during startup: {e}")


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


@app.get("/superclasses/{class_name}")
def get_superclasses_route(class_name: str):
    try:
        ontology = load_ontology()
        superclasses = fetch_superclasses(ontology, class_name)
        # return {"superclasses": [str(cls) for cls in superclasses]}
        return {"superclasses": superclasses}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred.")
