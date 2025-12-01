# How to use the ontology service in pynxtools

## Overview

The ontology service in `pynxtools` provides a FastAPI-based app for querying NeXus ontology integrated with ESRFET and PaNET. It enables users to retrieve ontological information, such as superclasses for NeXus Application definitions and makes datasets of different experimental techniques based on PaNET ontology findable in NOMAD.

## Prerequisites

- Python 3.8+
- Install required packages:
  - `pynxtools` and its dependencies (see [`pyproject.toml`](../../../pyproject.toml))
  - `owlready2`, `pygit2`, `fastapi`, `uvicorn`
- Ensure the NeXusOntology and definitions submodule are present in the repository, typically at [`src/pynxtools/NeXusOntology`](../../../src/pynxtools/NeXusOntology/) and [`src/pynxtools/definitions`](../../../src/pynxtools/definitions/) respectively.

## Getting Started

### Importing and Using the Service

The main entry point is the FastAPI app defined in [`pynxtools.nomad.apis.ontology_service`](../../../src/pynxtools//nomad/apis/ontology_service.py). You can import and use the service as follows:

```python
from pynxtools.nomad.apis.ontology_service import app, load_ontology, fetch_superclasses
```

### Minimal Working Example

You can extract superclasses for a NeXus class using the ontology service's HTTP API endpoint. For example, using Python's `requests` library:

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

This endpoint returns a JSON object with the list of superclasses for the given NeXus class name, as used internally in [pynxtools](../../../src/pynxtools/nomad/schema.py)

### Further Reading

- [Learn: Understanding the ontology service in pynxtools](../../learn/pynxtools/ontology-service.md)
