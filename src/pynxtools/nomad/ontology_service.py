######################################################################
######################## import libraries ############################
######################################################################
from fastapi import FastAPI, HTTPException
from owlready2 import get_ontology, sync_reasoner
from owlready2.namespace import Ontology
import os
import subprocess
from fastapi.responses import RedirectResponse

#######################################################################
########################## define app and functions ###################
#######################################################################
app = FastAPI()

# Define paths
NEXUS_ONTOLOGY_DIR = os.getenv("NEXUS_ONTOLOGY_DIR", "/home/nomad/work/NeXusOntology")
OWL_FILE_PATH = os.path.join(NEXUS_ONTOLOGY_DIR, "ontology", "NeXusOntology_full.owl")
SCRIPT_PATH = os.path.join(NEXUS_ONTOLOGY_DIR, "generate_ontology.sh")

def ensure_ontology_file():
    """
    Ensure the ontology file exists. If not, regenerate it using the script.
    """
    if not os.path.exists(OWL_FILE_PATH):
        try:
            print("Ontology file not found. Generating it...")
            subprocess.run(["bash", SCRIPT_PATH], check=True)
            print("Ontology file generated successfully.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to generate ontology file: {e}")

def load_ontology() -> Ontology:
    """
    Load the ontology file.
    """
    ensure_ontology_file()
    return get_ontology(OWL_FILE_PATH).load()

def fetch_superclasses(ontology, class_name):
    """
    Fetch superclasses for a given class name from the ontology.
    """
    cls = ontology.search_one(iri="*" + class_name)
    if cls is None:
        raise ValueError(f"Class '{class_name}' not found in the ontology.")
    all_superclasses = cls.ancestors()
    nexus_application_class = ontology.search_one(iri="*NeXusApplicationClass")
    if nexus_application_class is None:
        raise ValueError("Class 'NeXusApplicationClass' not found in the ontology.")
    unwanted_superclasses = {str(sc) for sc in nexus_application_class.ancestors()}
    print(f"Unwanted superclasses: {unwanted_superclasses}")
    filtered_superclasses = [sc for sc in all_superclasses if str(sc) not in unwanted_superclasses]
    return [str(sc).split('.')[-1] for sc in filtered_superclasses]

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

@app.get("/superclasses/{class_name}")
def get_superclasses_route(class_name: str):
    """
    API route to fetch superclasses for a given class name.
    """
    try:
        ontology = load_ontology()
        superclasses = fetch_superclasses(ontology, class_name)
        return {"superclasses": [str(cls) for cls in superclasses]}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")