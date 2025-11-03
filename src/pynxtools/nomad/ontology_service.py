######################################################################
######################## import libraries ############################
######################################################################
import os

from fastapi import FastAPI, HTTPException

os.environ["OWLREADY2_JAVA_LOG_LEVEL"] = "WARNING"
import logging
import subprocess

import pygit2
from fastapi.responses import RedirectResponse
from owlready2 import ThingClass, get_ontology, sync_reasoner
from owlready2.namespace import Ontology

from pynxtools.NeXusOntology.script.generate_ontology import main as generate_ontology

logger = logging.getLogger("pynxtools")

#######################################################################
########################## define app and functions ###################
#######################################################################
app = FastAPI(
    title="Ontology Service",
    description="A service to provide ontological information for a given NeXus class.",
)

# Define paths
local_dir = os.path.dirname(os.path.abspath(__file__))
ontology_dir = os.path.abspath(
    os.path.join(local_dir, "..", "NeXusOntology", "ontology")
)
OWL_FILE_PATH = None


def ensure_ontology_file():
    """
    Ensure the ontology file exists. If not, regenerate it using the Python function.
    """
    global OWL_FILE_PATH
    try:
        # Get the latest commit hash from the definitions submodule
        nexus_def_path = os.path.join(local_dir, "..", "definitions")
        repo = pygit2.Repository(nexus_def_path)
        latest_commit_hash = str(repo.head.target)[:7]

        # Construct the expected ontology file name
        owl_file_name = f"NeXusOntology_full_{latest_commit_hash}.owl"
        owl_file_path = os.path.join(ontology_dir, owl_file_name)
        # Check if the ontology file exists
        if not os.path.exists(owl_file_path):
            generate_ontology(
                full=True, nexus_def_path=nexus_def_path, def_commit=latest_commit_hash
            )
            # Rename the generated file to include the commit hash
            generated_file_path = os.path.join(
                ontology_dir, f"NeXusOntology_full_{latest_commit_hash}.owl"
            )
            os.rename(generated_file_path, owl_file_path)

        # Update the OWL_FILE_PATH to point to the correct file
        OWL_FILE_PATH = owl_file_path

    except Exception as e:
        raise RuntimeError(f"Failed to ensure ontology file: {e}")


def load_ontology() -> Ontology:
    try:
        ensure_ontology_file()
        base_name = os.path.basename(OWL_FILE_PATH).replace(".owl", "")
        inferred_owl_path = f"/tmp/{base_name}_inferred.owl"
        ontology = get_ontology(inferred_owl_path).load()
        return ontology
    except Exception as e:
        logger.error(f"Error loading ontology: {e}")
        raise


def get_label(entity):
    # Try to get rdfs:label, else fallback to name or IRI
    if hasattr(entity, "label") and entity.label:
        return entity.label[0]
    elif hasattr(entity, "name"):
        return entity.name
    else:
        return str(entity)


def build_hierarchy(ontology, class_name):
    """
    Returns the hierarchy from the given class up to the root as a nested dict.
    """
    cls = ontology.search_one(iri="*" + class_name)
    if cls is None:
        raise ValueError(f"Class '{class_name}' not found in the ontology.")

    def build_tree(node):
        parents = [sc for sc in node.is_a if isinstance(sc, ThingClass)]
        return {
            "label": get_label(node),
            "parent": [build_tree(parent) for parent in parents],
        }

    return build_tree(cls)


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


def fetch_subclasses(ontology, class_name):
    try:
        cls = ontology.search_one(iri="*" + class_name)
        if cls is None:
            raise ValueError(f"Class '{class_name}' not found in the ontology.")
        subclasses = cls.subclasses()
        filtered_subclasses = [
            sc
            for sc in subclasses
            if hasattr(sc, "iri")
            and (
                ("PaNET" in sc.iri) or ("nexusformat" in sc.iri) or ("ESRFET" in sc.iri)
            )
            and isinstance(sc, ThingClass)
        ]
        return [format_nxclass_label(sc) for sc in filtered_subclasses]
    except Exception as e:
        logger.error(f"Error in fetch_subclasses: {e}")
        raise


#######################################################################
########################## application routes #########################
#######################################################################
@app.on_event("startup")
def startup_event():
    """
    Ensure the ontology file is present during application startup.
    """
    try:
        ensure_ontology_file()
        base_name = os.path.basename(OWL_FILE_PATH).replace(".owl", "")
        inferred_owl_path = f"/tmp/{base_name}_inferred.owl"
        if not os.path.exists(inferred_owl_path):
            ontology = get_ontology(OWL_FILE_PATH).load()
            sync_reasoner(ontology)
            ontology.save(file=inferred_owl_path, format="rdfxml")
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


@app.get("/hierarchy/{class_name}")
def get_hierarchy_route(class_name: str):
    try:
        ontology = load_ontology()
        hierarchy = build_hierarchy(ontology, class_name)
        return hierarchy
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred.")


@app.get("/subclasses/{class_name}")
def get_subclasses_route(class_name: str):
    try:
        ontology = load_ontology()
        subclasses = fetch_subclasses(ontology, class_name)
        return {"subclasses": subclasses}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred.")
