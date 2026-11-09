# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Tests for the nomad-ontology-service client and Entry.techniques (new schema)."""

import pytest

try:
    from nomad.datamodel import EntryArchive, EntryMetadata
    from nomad.utils import get_logger
except ImportError:
    pytest.skip("nomad not installed", allow_module_level=True)

from pynxtools.nomad import ontology
from pynxtools.nomad.metainfo import _technique
from pynxtools.nomad.metainfo.base_classes.entry import Entry

INFO = {
    "url": "http://localhost:8000/nomad-oasis/ontology_service/nexus",
    "PaNET_methods_class": "PaNET01000",
    "NeXus_application_class": "NXapplication",
}

# Responses of the service routes, keyed by the path after INFO["url"].
RESPONSES = {
    "/superclasses/NXarpes": {
        "superclasses": ["NXarpes", "photoemission spectroscopy", "photon probe"]
    },
    "/descendants/PaNET01000": {"descendants": ["photoemission spectroscopy"]},
    "/descendants/NXapplication": {"descendants": ["NXarpes", "NXxps"]},
    "/class/NXarpes": {
        "comment": "Application definition for ARPES.",
        "see_also": "https://manual.nexusformat.org/classes/applications/NXarpes.html",
        "alt_labels": ["ARPES"],
        "properties": {"can_be_used_for_technique": ["ARPES"]},
    },
}


class FakeResponse:
    def __init__(self, status_code, body=None):
        self.status_code = status_code
        self._body = body

    def json(self):
        return self._body


def fake_get(responses):
    def get(url, **kwargs):
        path = url[len(INFO["url"]) :]
        if path in responses:
            return FakeResponse(200, responses[path])
        return FakeResponse(404, {"detail": "not found"})

    return get


def normalized_entry(monkeypatch, info, responses, definition="NXarpes"):
    monkeypatch.setattr(_technique, "get_ontology_service_info", lambda logger: info)
    monkeypatch.setattr(ontology.requests, "get", fake_get(responses))
    entry = Entry(definition=definition)
    archive = EntryArchive(data=entry, metadata=EntryMetadata(entry_name="test"))
    entry.normalize(archive, get_logger(__name__))
    return entry, archive


def test_entry_techniques(monkeypatch):
    entry, archive = normalized_entry(monkeypatch, INFO, RESPONSES)

    assert len(entry.techniques) == 1
    technique = entry.techniques[0]
    assert technique.name == "NXarpes"
    assert technique.description == "Application definition for ARPES."
    assert technique.see_also.endswith("NXarpes.html")
    assert technique.alt_labels == ["ARPES"]
    assert technique.properties == ["can_be_used_for_technique: ARPES"]

    eln = archive.results.eln
    # "photon probe" is neither a NeXus application nor a PaNET technique.
    assert "NXarpes" in eln.methods
    assert "photoemission spectroscopy" in eln.methods
    assert "photon probe" not in eln.methods
    assert "property:can_be_used_for_technique: ARPES" in eln.tags
    assert "Application definition for ARPES." in eln.descriptions


def test_entry_techniques_not_duplicated(monkeypatch):
    entry, archive = normalized_entry(monkeypatch, INFO, RESPONSES)
    entry.normalize(archive, get_logger(__name__))

    assert len(entry.techniques) == 1
    assert (
        archive.results.eln.tags.count("property:can_be_used_for_technique: ARPES") == 1
    )


def test_entry_without_service(monkeypatch):
    entry, archive = normalized_entry(monkeypatch, None, RESPONSES)

    assert entry.techniques == []
    assert not archive.results.eln.tags


def test_entry_without_definition(monkeypatch):
    entry, _ = normalized_entry(monkeypatch, INFO, RESPONSES, definition=None)

    assert entry.techniques == []


def test_failed_methods_request_falls_back_to_class_name(monkeypatch):
    responses = {k: v for k, v in RESPONSES.items() if "superclasses" not in k}
    entry, archive = normalized_entry(monkeypatch, INFO, responses)

    assert "NXarpes" in archive.results.eln.methods
    assert "photoemission spectroscopy" not in archive.results.eln.methods
    assert len(entry.techniques) == 1


def test_service_not_installed(monkeypatch):
    class ConfigWithoutService:
        def get_plugin_entry_point(self, entry_point_id):
            raise KeyError(entry_point_id)

    monkeypatch.setattr(ontology, "config", ConfigWithoutService())

    assert ontology.get_ontology_service_info(get_logger(__name__)) is None
