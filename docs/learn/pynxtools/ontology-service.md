# Understanding the ontology service in pynxtools

!!! info "This is a learn guide for using the ontology service. If you want to learn more about how to use `ontology service` in `pynxtools`, please visit the [how-to guide](../../how-tos/pynxtools/ontology-service.md)."

## Introduction

The ontology service in `pynxtools` provides a [FastAPI](https://fastapi.tiangolo.com/)-based app for querying the [NeXusOntology](https://github.com/nexusformat/NeXusOntology). This service enables users to retrieve semantic contextualization—such as superclasses for NeXus application definitions—and makes datasets of different experimental techniques findable in NOMAD.

The NeXus ontology integrates two key experimental technique ontologies:

- **[PaN Experimental Technique Ontology (PaNET)](https://bioportal.bioontology.org/ontologies/PANET)**: Photon and Neutron Experimental Techniques ontology (PaNET) provides a standardized vocabulary for describing experimental techniques used at photon and neutron research facilities, enabling consistent categorization and discovery of scientific data across different institutions.

- **[ESRF Experimental Technique Ontology (ESRFET)](https://github.com/pan-ontologies/esrf-ontologies)**: An ontology developed by the European Synchrotron Radiation Facility (ESRF) to classify and describe experimental techniques specific to synchrotron radiation science. It complements PaNET by providing more granular terms for synchrotron-based methods.

By using these ontologies, the service maps terms that are defined in NeXus application definitions to standardized terms for experimental techniques, improving data interoperability and enabling semantic search capabilities within NOMAD.

## How it fits in pynxtools

The `ontology service` itself lives in the standalone [`nomad-ontology-service`](https://github.com/FAIRmat-NFDI/nomad-ontology-service) plugin, not in `pynxtools`. It is registered as an [`APIEntryPoint`](https://nomad-lab.eu/prod/v1/docs/reference/config.html#apientrypoint), which allows NOMAD to automatically discover and mount its FastAPI routes at startup. `pynxtools` is a *consumer* of this service: it prepares the ontology file the service reads, and queries the service's HTTP API during processing to attach semantic technique metadata to NeXus entries.

## Core concepts

- **Ontology**: A formal representation of concepts (classes), relationships, and properties, typically serialized as [OWL](https://www.w3.org/OWL/) files.
- **Name of an application definition**: A symbol describing an experimental technique in NeXus (e.g., `NXmpes_arpes`).
- **Relation**: A connection between entities, such as a superclass/subclass relationship. 
- **Inferred ontology**: An ontology file that has been processed by a reasoner to infer additional relationships and properties between classes, beyond those explicitly defined in the original ontology.

Ontologies are represented as OWL files (e.g., `NeXusOntology_full_<release-version>_inferred.owl`) and loaded using `owlready2`.

## Architecture & design

- **Main modules**:
    - `nomad_ontology_service.apis.app` (in the [`nomad-ontology-service`](https://github.com/FAIRmat-NFDI/nomad-ontology-service) plugin): FastAPI app, core logic for loading and querying ontologies.
    - `pynxtools.nomad.ensure_ontology_initialization`: Downloads the pinned [NeXusOntology release](https://github.com/FAIRmat-NFDI/NeXusOntology/releases), merges in the configured `imports` (e.g. ESRFET, PaNET), and runs the reasoner to produce the inferred ontology file.
    - `pynxtools.nomad.schema_packages.schema`: Triggers the ontology query during entry normalization (`NexusMeasurement.normalize`) and stores the results in NOMAD Metainfo.
- **Key functions**:
    - `ensure_ontology_initialization(ontology_imports)` (pynxtools): Ensures the inferred ontology file is present, downloading and reasoning over it if needed.
    - `_fetch_superclasses(ontology, class_name, cfg)` / `_fetch_descendants(ontology, class_name, cfg)` (nomad-ontology-service): Traverse the loaded ontology for a given class.
- **Data flow**:
    - During normalization, `pynxtools` calls `ensure_ontology_initialization`, which downloads the base NeXusOntology release (if not already cached), merges in the configured `imports`, runs the reasoner, and writes the inferred ontology file.
    - On each request, `nomad-ontology-service` loads that inferred ontology fresh via `owlready2`.
    - Its API endpoints query the loaded ontology for relationships and metadata.

## Extensibility points

- Extend FastAPI routes in [`apis/app.py`](https://github.com/FAIRmat-NFDI/nomad-ontology-service/blob/main/src/nomad_ontology_service/apis/app.py) (in the `nomad-ontology-service` plugin) for new queries.

## Examples

```python
import requests

# Replace with the actual running service URL and configured ontology name
base_url = "http://localhost:8000/nomad-oasis/ontology_service"
ontology_name = "nexus"
class_name = "NXmpes_arpes"
response = requests.get(f"{base_url}/{ontology_name}/superclasses/{class_name}")
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
