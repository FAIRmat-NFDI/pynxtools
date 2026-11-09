# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""
Client for nomad-ontology-service, shared by the old (``schema_packages``) and
the new (``metainfo``) NeXus schemas.

The service is an optional dependency (``pynxtools[ontology]``): if it is not
installed or has no ontology registered, ``get_ontology_service_info`` returns
``None`` and callers skip the ontology enrichment.
"""

from __future__ import annotations

from typing import Any

import requests

try:
    from nomad.config import config
    from nomad.datamodel.results import ELN, Results
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

from pynxtools.nomad import ensure_ontology_initialization

ONTOLOGY_SERVICE_ENTRY_POINT = "nomad_ontology_service:ontology_service"


def get_ontology_service_info(logger) -> dict[str, Any] | None:
    """Return the service URL and NeXus/PaNET root classes of the first
    registered ontology, after making sure the NeXus ontology file exists.

    Returns ``None`` if the service is not installed, has no ontology
    registered, or the ontology could not be initialized.
    """
    try:
        ep = config.get_plugin_entry_point(ONTOLOGY_SERVICE_ENTRY_POINT)
    except KeyError:
        return None
    if not ep.ontologies:
        return None

    ontology = ep.ontologies[0]
    try:
        ensure_ontology_initialization(ontology_imports=ontology.imports)
    except Exception as e:
        logger.warning(f"Could not initialize ontology for ontology service: {e}")
        return None

    base = config.services.api_base_path.rstrip("/")
    prefix = ep.prefix.strip("/")
    return {
        "url": f"http://localhost:8000{base}/{prefix}/{ontology.name}",
        "PaNET_methods_class": ontology.PaNET_methods_class,
        "NeXus_application_class": ontology.NeXus_application_class,
    }


def _get_json(url: str, logger) -> dict | None:
    """GET ``url`` and return the JSON body, or ``None`` on any failure."""
    try:
        response = requests.get(url)
    except requests.RequestException as e:
        logger.warning(f"Ontology service request failed for {url}: {e}")
        return None
    if response.status_code != 200:
        logger.warning(f"Ontology service returned {response.status_code} for {url}.")
        return None
    try:
        return response.json()
    except ValueError as e:
        logger.warning(f"Ontology service returned invalid JSON for {url}: {e}")
        return None


def fetch_methods(info: dict[str, Any], class_name: str, logger) -> list[str] | None:
    """Return the superclasses of ``class_name`` that are NeXus application
    definitions or PaNET techniques, or ``None`` if a request failed."""
    superclasses_response = _get_json(
        f"{info['url']}/superclasses/{class_name}", logger
    )
    panet = _get_json(
        f"{info['url']}/descendants/{info['PaNET_methods_class']}", logger
    )
    nexus_applications = _get_json(
        f"{info['url']}/descendants/{info['NeXus_application_class']}", logger
    )
    if superclasses_response is None or panet is None or nexus_applications is None:
        return None

    superclasses = set(superclasses_response.get("superclasses", []))
    valid_methods = (superclasses & set(nexus_applications.get("descendants", []))) | (
        superclasses & set(panet.get("descendants", []))
    )
    return sorted(valid_methods)


def fetch_technique(info: dict[str, Any], class_name: str, logger) -> dict | None:
    """Return the technique metadata of ``class_name`` as keyword arguments for
    a technique section, or ``None`` if the class could not be fetched."""
    class_info = _get_json(f"{info['url']}/class/{class_name}", logger)
    if class_info is None:
        return None
    return {
        "name": class_name,
        "description": class_info.get("comment"),
        "see_also": class_info.get("see_also"),
        "alt_labels": class_info.get("alt_labels", []),
        "properties": [
            f"{prop}: {value}"
            for prop, values in class_info.get("properties", {}).items()
            for value in values
        ],
    }


def add_to_results_eln(
    archive,
    methods: list[str] | None = None,
    tags: list[str] | None = None,
    descriptions: list[str] | None = None,
) -> None:
    """Append values to ``archive.results.eln``, skipping duplicates."""
    if archive.results is None:
        archive.results = Results()
    if archive.results.eln is None:
        archive.results.eln = ELN()
    eln = archive.results.eln
    for quantity, values in (
        ("methods", methods),
        ("tags", tags),
        ("descriptions", descriptions),
    ):
        if not values:
            continue
        if getattr(eln, quantity) is None:
            setattr(eln, quantity, [])
        existing = getattr(eln, quantity)
        for value in values:
            if value not in existing:
                existing.append(value)


def add_technique_to_results_eln(archive, technique: dict) -> None:
    """Index technique metadata in ``archive.results.eln`` so it is searchable:
    short facts as exact-match tags, the free-text comment as a description."""
    add_to_results_eln(
        archive,
        tags=[f"property:{prop}" for prop in technique["properties"]],
        descriptions=[technique["description"]] if technique["description"] else None,
    )
