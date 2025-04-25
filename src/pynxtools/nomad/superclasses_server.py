
######################################################################
######################## import libraries ############################
######################################################################
from fastapi import FastAPI, HTTPException
from owlready2 import get_ontology, sync_reasoner
from owlready2.namespace import Ontology
import os
from fastapi.responses import RedirectResponse

#######################################################################
########################## define app and functions ###################
#######################################################################
app = FastAPI()

def load_ontology(*args) -> Ontology:
    owl_file = os.path.join(os.path.dirname(__file__), *args)
    return get_ontology(owl_file).load()

def fetch_superclasses(ontology, class_name):
    # Search for the first IRI ending with the class name
    cls = ontology.search_one(iri="*" + class_name)
    if cls is None:
        raise ValueError(f"Class '{class_name}' not found in the ontology.")
    all_superclasses =  cls.ancestors()
    #filter unwantedsuperclasses
    unwanted_superclasses = {
        "NeXusOntology_full.NeXusObject",
        "owl.Thing",
        "NeXusOntology_full.NeXus",
        "NeXusOntology_full.NeXusApplicationClass"}
    filtered_superclasses = [sc for sc in all_superclasses if str(sc) not in unwanted_superclasses]
    filtered_superclasses = [str(sc).split('.')[-1] for sc in filtered_superclasses]
    return filtered_superclasses
#######################################################################
########################## application routes #########################
#######################################################################
@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/superclasses/{ontology_name}/{class_name}")
def get_superclasses_route(ontology_name: str, class_name: str):
    try:
        ontology = load_ontology(ontology_name)

        superclasses = fetch_superclasses(ontology, class_name)

        return {"superclasses": [str(cls) for cls in superclasses]}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
