# Understanding the ontology service in pynxtools

!!! info "This is a learn guide for using the ontology service. If you want to learn more about how to use `ontology service` in `pynxtools`, please visit the [how-to guide](../../how-tos/pynxtools/ontology-service.md)."

## Introduction

The ontology service in `pynxtools` provides a [FastAPI](https://fastapi.tiangolo.com/)-based app for querying the [NeXusOntology](https://github.com/nexusformat/NeXusOntology). This service enables users to retrieve semantic contextualization—such as superclasses for NeXus application definitions—and makes datasets of different experimental techniques findable in NOMAD.

The NeXus ontology integrates two key experimental technique ontologies:

- **[PaN Experimental Technique Ontology (PaNET)](https://bioportal.bioontology.org/ontologies/PANET)**: Photon and Neutron Experimental Techniques ontology (PaNET) provides a standardized vocabulary for describing experimental techniques used at photon and neutron research facilities, enabling consistent categorization and discovery of scientific data across different institutions.

- **[ESRF Experimental Technique Ontology (ESRFET)](https://github.com/pan-ontologies/esrf-ontologies)**: An ontology developed by the European Synchrotron Radiation Facility (ESRF) to classify and describe experimental techniques specific to synchrotron radiation science. It complements PaNET by providing more granular terms for synchrotron-based methods.

By using these ontologies, the service maps terms that are defined in NeXus application definitions to standardized terms for experimental techniques, improving data interoperability and enabling semantic search capabilities within NOMAD.

## How it fits in pynxtools

The `ontology service` only operates when `pynxtools` is run within `NOMAD`. It is registered as an [`APIEntryPoint`](https://nomad-lab.eu/prod/v1/docs/reference/config.html#apientrypoint), which allows NOMAD to automatically discover and mount the FastAPI routes at startup. The service exposes the [NeXusOntology](https://github.com/nexusformat/NeXusOntology) to users and connected systems.

## Core concepts

- **Ontology**: A formal representation of concepts (classes), relationships, and properties, typically serialized as [OWL](https://www.w3.org/OWL/) files.
- **Name of an application definition**: A symbol describing an experimental technique in NeXus (e.g., `NXmpes_arpes`).
- **Relation**: A connection between entities, such as a superclass/subclass relationship. 
- **Inferred ontology**: An ontology file that has been processed by a reasoner to infer additional relationships and properties between classes, beyond those explicitly defined in the original ontology.

Ontologies are represented as OWL files (e.g., `NeXusOntology_full_<commit>_inferred.owl`) and loaded using `owlready2`.

## Architecture & design

- **Main modules**:
    - `pynxtools.nomad.apis.ontology_service`: FastAPI app, core logic for loading and querying ontologies.
    - `pynxtools.NeXusOntology.script.generate_ontology`: Generates ontology files from NeXus definitions.
    - `pynxtools.nomad.schema`: Initializes [NOMAD Metainfo](https://nomad-lab.eu/prod/v1/docs/explanation/data.html#schema) and schema integration..
- **Key classes/functions**:
    - `load_ontology()`: Loads the inferred ontology file.
    - `fetch_superclasses(ontology, class_name)`: Retrieves superclasses for a given NeXus class.
    - `ensure_ontology_file()`: Ensures an ontology file is present and up-to-date.
- **Data flow**:
    - On startup, the service verifies whether the inferred ontology file exists; if absent, it runs the reasoner and generates the inferred ontology file.
    - Inferred ontology is loaded via `owlready2`.
    - API endpoints query this inferred ontology for relationships and metadata.

## Extensibility points

- Extend FastAPI routes in [`ontology_service.py`](https://github.com/FAIRmat-NFDI/pynxtools/blob/ontology-service/src/pynxtools/nomad/apis/ontology_service.py) for new queries.

## Examples

```python
import requests

# Replace with the actual running service URL
base_url = "http://localhost:8000/nomad-oasis/"
class_name = "NXmpes_arpes"
response = requests.get(f"{base_url}/superclasses/{class_name}")
if response.status_code == 200:
  superclasses = response.json().get("superclasses", [])
  print(superclasses)
else:
  print(f"Error: {response.status_code} - {response.text}")
```

## Glossary

- **NeXus**: A common data format for neutron, X-ray, and muon science.
- **OWL**: Web Ontology Language, used for representing ontologies.
- **Ontology**: Structured representation of concepts and relationships.
- **Superclass**: A parent class in the ontology hierarchy.
- **Reasoner**: Tool for inferring new relationships in an ontology.
- **NOMAD**: The FAIRmat NOMAD project for materials data.
