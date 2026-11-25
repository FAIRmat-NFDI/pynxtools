# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""
NeXus NOMAD metainfo: public API and schema package entry points.

Schema packages are scoped per scientific technique (one `SchemaPackage` per
`packages` key below) rather than one monolithic schema. `packages` maps
each technique to the application definition modules that belong to it.
Base classes aren't split (`_base_classes_stems()` lists them from disk).
Application modules not listed in `packages` don't fit a specific category
and are only reachable through `NexusApplicationsEntryPoint`.
"""

from __future__ import annotations

import importlib
from pathlib import Path

from nomad.config.models.plugins import SchemaPackageEntryPoint
from nomad.metainfo import SchemaPackage

_BASE_CLASSES_DIR = Path(__file__).parent / "base_classes"
# Derived from this module's own __name__, not hardcoded, so this stays
# correct if this package is ever moved.
_APPLICATIONS_MODULE = f"{__name__}.applications"
_BASE_CLASSES_MODULE = f"{__name__}.base_classes"

packages: dict[str, list[str]] = {
    "apm": [
        "apm",
        "apm_compositionspace_config",
        "apm_compositionspace_results",
        "apm_paraprobe_clusterer_config",
        "apm_paraprobe_clusterer_results",
        "apm_paraprobe_distancer_config",
        "apm_paraprobe_distancer_results",
        "apm_paraprobe_intersector_config",
        "apm_paraprobe_intersector_results",
        "apm_paraprobe_nanochem_config",
        "apm_paraprobe_nanochem_results",
        "apm_paraprobe_ranger_config",
        "apm_paraprobe_ranger_results",
        "apm_paraprobe_selector_config",
        "apm_paraprobe_selector_results",
        "apm_paraprobe_spatstat_config",
        "apm_paraprobe_spatstat_results",
        "apm_paraprobe_surfacer_config",
        "apm_paraprobe_surfacer_results",
        "apm_paraprobe_tessellator_config",
        "apm_paraprobe_tessellator_results",
        "apm_paraprobe_tool_config",
        "apm_paraprobe_tool_results",
    ],
    "xas": [
        "xas",
        "xas_herfd",
        "xas_pey",
        "xas_pfy",
        "xas_tey",
        "xas_tfy",
        "xas_trans",
        "xasproc",
    ],
    "diffraction": [
        "azint1d",
        "azint2d",
        "monopd",
        "xbase",
        "xeuler",
        "xkappa",
        "xlaue",
        "xlaueplate",
        "xnb",
        "xrd",
        "xrd_pan",
        "xrot",
    ],
    "tof": [
        "directtof",
        "indirecttof",
        "lauetof",
        "reftof",
        "sastof",
        "tofnpd",
        "tofraw",
        "tofsingle",
    ],
    "sas": ["cansas", "iqproc", "sas"],
    "optical_spectroscopy": [
        "dispersive_material",
        "ellipsometry",
        "optical_spectroscopy",
        "raman",
        "transmission",
    ],
    "spm": ["afm", "spm", "stm", "sts"],
    "photoemission": ["arpes", "mpes", "mpes_arpes", "xps"],
    "em": ["em", "em_calorimetry"],
    "tomography": ["cxi_ptycho", "stxm", "tomo", "tomophase", "tomoproc"],
    "microstructure": [
        "microstructure_kanapy_results",
        "microstructure_score_config",
        "microstructure_score_results",
    ],
    "neutron": ["snsevent", "snshisto", "spe", "sqom", "tas"],
    "scan": ["iv_temp", "refscan", "scan", "sensor_scan"],
}
# Application definition modules with no siblings are not split into their own
# single-entry technique groups and stay out of `packages`.
# They are only reachable through the general NexusApplicationsEntryPoint.

_package_cache: dict[str, SchemaPackage] = {}


def _is_generated_section(obj: object, module_name: str) -> bool:
    """Return True if obj is a Section definition generated in this module."""
    from nomad.metainfo.metainfo import Section as NomadSection

    m_def = getattr(obj, "m_def", None)
    if not isinstance(m_def, NomadSection):
        return False
    return getattr(obj, "__module__", None) == module_name


def _build_package(
    technique: str, stems: list[str], module_prefix: str
) -> SchemaPackage:
    """Import every application definition's module name in ``stems`` and
    assemble them into one shared SchemaPackage.

    Cached per technique: calling this again for the same technique is cheap.
    """
    if technique in _package_cache:
        return _package_cache[technique]

    m_package = SchemaPackage(name=f"{__name__}.{technique}")
    for stem in stems:
        module_name = f"{module_prefix}.{stem}"
        # Import first, assign m_package after. If we assigned m_package to
        # the module before this import, the import would undo it: NOMAD
        # renames a module's package to that module's own path (e.g.
        # "...applications.apm") the moment a class in it gets defined.
        mod = importlib.import_module(module_name)
        setattr(mod, "m_package", m_package)
        for attr_name in dir(mod):
            obj = getattr(mod, attr_name, None)
            if _is_generated_section(obj, module_name):
                m_package.section_definitions.append(obj.m_def)
    m_package.__init_metainfo__()

    _package_cache[technique] = m_package
    return m_package


def _base_classes_stems() -> list[str]:
    """Return all generated base_classes module stems."""
    return sorted(
        p.stem for p in _BASE_CLASSES_DIR.glob("*.py") if p.stem != "__init__"
    )


def _ungrouped_application_stems() -> list[str]:
    """Return application stems not assigned to any technique in `packages`."""
    grouped = {stem for stems in packages.values() for stem in stems}
    all_stems = {
        p.stem
        for p in (Path(__file__).parent / "applications").glob("*.py")
        if p.stem != "__init__"
    }
    return sorted(all_stems - grouped)


class NexusBaseClassesEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package(
            "base_classes", _base_classes_stems(), _BASE_CLASSES_MODULE
        )


class ApmSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package("apm", packages["apm"], _APPLICATIONS_MODULE)


class XasSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package("xas", packages["xas"], _APPLICATIONS_MODULE)


class DiffractionSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package(
            "diffraction", packages["diffraction"], _APPLICATIONS_MODULE
        )


class TofSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package("tof", packages["tof"], _APPLICATIONS_MODULE)


class SasSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package("sas", packages["sas"], _APPLICATIONS_MODULE)


class OpticalSpectroscopySchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package(
            "optical_spectroscopy",
            packages["optical_spectroscopy"],
            _APPLICATIONS_MODULE,
        )


class SpmSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package("spm", packages["spm"], _APPLICATIONS_MODULE)


class PhotoemissionSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package(
            "photoemission", packages["photoemission"], _APPLICATIONS_MODULE
        )


class EmSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package("em", packages["em"], _APPLICATIONS_MODULE)


class TomographySchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package(
            "tomography", packages["tomography"], _APPLICATIONS_MODULE
        )


class MicrostructureSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package(
            "microstructure", packages["microstructure"], _APPLICATIONS_MODULE
        )


class NeutronSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package("neutron", packages["neutron"], _APPLICATIONS_MODULE)


class ScanSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        return _build_package("scan", packages["scan"], _APPLICATIONS_MODULE)


def load_all_packages() -> None:
    """Import every base-class and application module and assemble all packages.

    Idempotent: `_build_package()` caches per technique, so calling this more
    than once is safe.
    """
    _build_package("base_classes", _base_classes_stems(), _BASE_CLASSES_MODULE)
    for technique, stems in packages.items():
        _build_package(technique, stems, _APPLICATIONS_MODULE)
    _build_package("applications", _ungrouped_application_stems(), _APPLICATIONS_MODULE)


def any_entry_point_loaded() -> bool:
    """Return True if any base_classes/application package is already registered.

    Checking `base_classes` alone would be wrong: a deployment can enable
    application techniques while disabling base_classes, or vice versa.
    """
    from nomad.metainfo.metainfo import Package

    return any(
        f"{__name__}.{key}" in Package.registry
        for key in ("base_classes", "applications", *packages)
    )


class NexusApplicationsEntryPoint(SchemaPackageEntryPoint):
    """Overarching schema for all application technique."""

    def load(self):
        load_all_packages()
        # Marker only; nothing reads load()'s return value. It exists purely
        # to trigger the imports above.
        return SchemaPackage(name=_APPLICATIONS_MODULE)


nexus_base_classes = NexusBaseClassesEntryPoint(
    name="NeXus Base Classes",
    description=("NOMAD Metainfo Section classes for all NeXus base classes."),
)

nexus_applications = NexusApplicationsEntryPoint(
    name="NeXus Application Definitions",
    description=(
        "NOMAD Metainfo Section classes for all NeXus application definitions."
    ),
)

apm = ApmSchemaPackageEntryPoint(
    name="Atom probe microscopy",
    description="Atom probe microscopy (APM) NeXus application definitions.",
)

xas = XasSchemaPackageEntryPoint(
    name="X-ray absorption spectroscopy",
    description="X-ray absorption spectroscopy (XAS) NeXus application definitions.",
)

diffraction = DiffractionSchemaPackageEntryPoint(
    name="Diffraction",
    description=(
        "Single-crystal/powder diffraction and azimuthal-integration NeXus "
        "application definitions."
    ),
)

tof = TofSchemaPackageEntryPoint(
    name="Time-of-Flight Neutron Scattering",
    description="Time-of-flight neutron scattering NeXus application definitions.",
)

sas = SasSchemaPackageEntryPoint(
    name="Small-angle scattering",
    description="Small-angle scattering (SAS) NeXus application definitions.",
)

optical_spectroscopy = OpticalSpectroscopySchemaPackageEntryPoint(
    name="Optical Spectroscopy",
    description=(
        "Optical spectroscopy (ellipsometry, Raman, UV-Vis transmission, ...) "
        "NeXus application definitions."
    ),
)

spm = SpmSchemaPackageEntryPoint(
    name="Scanning probe microscopy",
    description="Scanning probe microscopy (AFM/STM/STS) NeXus application definitions.",
)

photoemission = PhotoemissionSchemaPackageEntryPoint(
    name="Photoemission spectroscopy",
    description=(
        "Photoemission spectroscopy (XPS/ARPES/MPES) NeXus application definitions."
    ),
)

em = EmSchemaPackageEntryPoint(
    name="Electron Microscopy",
    description="Electron microscopy (EM) NeXus application definitions.",
)

tomography = TomographySchemaPackageEntryPoint(
    name="Tomography and scanning transmission imaging",
    description="Tomography and scanning transmission imaging NeXus application definitions.",
)

microstructure = MicrostructureSchemaPackageEntryPoint(
    name="NeXus Microstructure",
    description="Microstructure modelling NeXus application definitions.",
)

neutron = NeutronSchemaPackageEntryPoint(
    name="Neutron Scattering",
    description=(
        "Neutron scattering (triple-axis, S(q,omega), SNS event/histogram) "
        "NeXus application definitions."
    ),
)

scan = ScanSchemaPackageEntryPoint(
    name="Scan and Sensor Scan",
    description="Generic scan/sensor-scan NeXus application definitions.",
)
