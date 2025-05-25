######################################################################
######################## import libraries ############################
######################################################################
from fastapi import FastAPI, HTTPException
from owlready2 import get_ontology, sync_reasoner
from owlready2.namespace import Ontology
import os
import subprocess
from fastapi.responses import RedirectResponse
from ..NeXusOntology.script.generate_ontology import main as generate_ontology
import logging
import pygit2

#######################################################################
########################## define app and functions ###################
#######################################################################
app = FastAPI()

# Define paths
local_dir = os.path.dirname(os.path.abspath(__file__))
nexusontology_dir = os.path.abspath(os.path.join(local_dir, "..", "NeXusOntology"))
ontology_dir = os.path.join(nexusontology_dir, "ontology")
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
            print(f"Ontology file '{owl_file_name}' not found. Generating it...")
            generate_ontology(full=True, nexus_def_path=nexus_def_path, def_commit=latest_commit_hash)
            # Rename the generated file to include the commit hash
            generated_file_path = os.path.join(ontology_dir, f"NeXusOntology_full_{latest_commit_hash}.owl")	
            os.rename(generated_file_path, owl_file_path)
            print(f"Ontology file generated and saved as '{owl_file_name}'.")

        # Update the OWL_FILE_PATH to point to the correct file
        OWL_FILE_PATH = owl_file_path

    except Exception as e:
        raise RuntimeError(f"Failed to ensure ontology file: {e}")

def load_ontology() -> Ontology:
    try:
        ensure_ontology_file()
        return get_ontology(OWL_FILE_PATH).load()
    except Exception as e:
        print(f"Error loading ontology: {e}")
        raise

def fetch_superclasses(ontology, class_name):
    try:
        cls = ontology.search_one(iri="*" + class_name)
        if cls is None:
            raise ValueError(f"Class '{class_name}' not found in the ontology.")
        all_superclasses = cls.ancestors()
        nexus_application_class = ontology.search_one(iri="*NeXusApplicationClass")
        if nexus_application_class is None:
            raise ValueError("Class 'NeXusApplicationClass' not found in the ontology.")
        unwanted_superclasses = {str(sc) for sc in nexus_application_class.ancestors()}
        filtered_superclasses = [sc for sc in all_superclasses if str(sc) not in unwanted_superclasses]
        return [str(sc).split('.')[-1] for sc in filtered_superclasses]
    except Exception as e:
        print(f"Error in fetch_superclasses: {e}")
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
    except RuntimeError as e:
        print(f"Error during startup: {e}")

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

import logging
logging.basicConfig(level=logging.DEBUG)

@app.get("/superclasses/{class_name}")
def get_superclasses_route(class_name: str):
    logging.debug(f"Received request for class_name: {class_name}")
    try:
        ontology = load_ontology()
        logging.debug("Ontology loaded successfully.")
        superclasses = fetch_superclasses(ontology, class_name)
        logging.debug(f"Fetched superclasses: {superclasses}")
        return {"superclasses": [str(cls) for cls in superclasses]}
    except ValueError as e:
        logging.error(f"ValueError: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")