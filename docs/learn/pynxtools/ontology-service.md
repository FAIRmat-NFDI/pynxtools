# Understanding the ontology service in pynxtools

## Introduction

The ontology service in `pynxtools` addresses the need for structured, semantic search of NeXus Application definitions and their relationships to ESRFET and PaNET, within NOMAD. It enables querying, reasoning of ontologies, supporting FAIR data principles in scientific workflows.

## How It Fits in pynxtools

This service operates within the `nomad` integration layer, exposing ontological data for NeXus Application definitions through a FastAPI interface. It works by accessing ontology files, leveraging NOMAD configuration, and processing NeXus definitions to provide semantic tools and data to users and connected systems.

## Core Concepts

- **Ontology**: A formal representation of concepts (classes), relationships, and properties, typically serialized as OWL files.
- **Application definition**: A class or term describing an experimental technique in the NeXus (e.g., `NXiv_temp`).
- **Relation**: Connections between entities, such as superclass/subclass relationships.
- **Inferred ontology**: An ontology file that has been processed by a reasoner to infer additional relationships and properties between classes, beyond those explicitly defined. 

Ontologies are represented as OWL files (e.g., `NeXusOntology_full_<commit>_inferred.owl`) and loaded using `owlready2`.

## Architecture & Design

- **Main Modules**:
  - `pynxtools.nomad.apis.ontology_service`: FastAPI app, core logic for loading and querying ontologies.
  - `pynxtools.NeXusOntology.script.generate_ontology`: Generates ontology files from NeXus definitions.
  - `pynxtools.nomad.schema`: Initializes metainfo and schema integration.
- **Key Classes/Functions**:
  - `load_ontology()`: Loads the inferred ontology file.
  - `fetch_superclasses(ontology, class_name)`: Retrieves superclasses for a given NeXus class.
  - `ensure_ontology_file()`: Ensures ontology file is present and up-to-date.
- **Data Flow**:
  1. On startup, the service verifies whether the inferred ontology file exists; if absent, it runs the reasoner and generates the inferred ontology file.
  2. Inferred ontology is loaded via `owlready2`.
  3. API endpoints query this inferred ontology for relationships and metadata.

## Extensibility Points

- Extend FastAPI routes in `ontology_service.py` for new queries.

## Examples

```python
import requests

# Replace with the actual running service URL
base_url = "http://localhost:8000/nomad-oasis/"
class_name = "NXiv_temp"
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
