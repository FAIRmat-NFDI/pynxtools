# pynxtools and NOMAD

`pynxtools` was built both as a standalone NeXus toolkit and as a plugin to the
**NOMAD** research data management platform. This page explains how the two pieces fit together and what happens to a NeXus file inside NOMAD.

---

## What NOMAD provides

[NOMAD](https://nomad-lab.eu/) is an open-source research data management system
developed within the FAIRmat consortium. It covers the *findable* and *accessible* dimensions of FAIR that NeXus itself does not address:

| FAIR dimension | Covered by |
|----------------|-----------|
| Findable | NOMAD (persistent identifiers, rich metadata indexing) |
| Accessible | NOMAD (public REST API, web interface, persistent URLs) |
| Interoperable | NeXus + pynxtools (standardized format and definitions) |
| Reusable | NeXus + pynxtools (application definitions, rich provenance) |

NOMAD is available as:

- **Public instance** — [nomad-lab.eu](https://nomad-lab.eu/prod/v1/gui/) — hosted by  FAIRmat/FHI, free for research use.
- [**NOMAD OASIS**](https://nomad-lab.eu/nomad-lab/nomad-oasis.html) — a self-hosted deployment for institutions that need local data control, privacy, or integration with existing IT infrastructure.

---

## How pynxtools plugs into NOMAD

`pynxtools` integrates with NOMAD through the
[NOMAD plugin system](https://nomad-lab.eu/prod/v1/docs/howto/plugins/plugins.html). When both `pynxtools` and `nomad-lab` are installed in the same Python environment, NOMAD automatically discovers and loads `pynxtools` as a plugin at startup.

The plugin registers:

1. **A parser** (`NexusParser`) — called for any file with extension `.nxs` or `.hdf5` (when the file has an HDF5 attribute named `NX_class` at the root level with the value `NXroot`).
2. **Schema extensions** — the NeXus definitions bundled with pynxtools are translated into NOMAD's internal schema language (*Metainfo*), making all NeXus concepts searchable.
3. **A normalizer** — runs after parsing to extract NOMAD-searchable quantities such as the measurement technique and object identifiers.

### The parsing pipeline

When NOMAD encounters a `.nxs` file:

```
.nxs file
    │
    ▼
NexusParser.parse()                        ← pynxtools/nomad/parser.py
    │  creates nexus_schema.Root()
    │  sets archive.data = nx_root
    │
    ▼
HandleNexus(logger, mainfile)              ← pynxtools/nexus/nexus.py
    .process_nexus_master_file(callback)
    │  traverses the HDF5 tree
    │  resolves each node against NXDL definitions
    │  calls _nexus_populate() for every field / attribute
    │
    ▼
NexusParser._nexus_populate(params)        ← callback in parser.py
    │  maps HDF5 path → Metainfo sections + quantities
    │  via _to_section() and _populate_data()
    │
    ▼
NexusParser.parse() — post-processing      ← after full traversal
    │  reads /ENTRY/definition → archive.metadata.entry_type
    │  extracts chemical formulas from NXsample / NXsubstance
    │  sets archive.metadata.domain = "nexus"
    │
    ▼
NOMAD archive (searchable, versioned, indexed)
```

### What ends up in NOMAD

After parsing, your NeXus data is available in NOMAD as:

| Component | What it shows |
|-----------|--------------|
| **H5Web viewer** | Interactive HDF5 file browser on the entry Overview page |
| **DATA tab** | Normalized metadata extracted by the parser and normalizers |
| **Search index** | All Metainfo quantities that NOMAD has indexed for cross-dataset comparison |
| **API** | Raw archive JSON accessible via the REST API |

The key quantities indexed by the NeXus normalizer depend on the application definition: common entries include technique name (`definition`), sample identifiers, start time, and instrument names.

---

## Metainfo: NeXus definitions as a NOMAD schema

NOMAD uses its own schema language (*Metainfo*) to describe data structures. When `pynxtools` is loaded as a plugin, all NeXus base classes and application definitions bundled with it are compiled into NOMAD Metainfo sections.

This means:

- Every NeXus field becomes a Metainfo quantity with the correct type and unit.
- Every NeXus base class becomes a NOMAD section.
- The application definition specifies which sections and quantities are required.

The compiled Metainfo can be viewed in the NOMAD GUI at:
`Analyze → Metainfo → pynxtools`

---

## Installation

To use `pynxtools` with NOMAD, install both packages in the same environment:

=== "uv"

    ```bash
    uv pip install pynxtools nomad-lab
    ```

=== "pip"


    ```bash
    pip install --upgrade pip
    pip install pynxtools nomad-lab
    ```


For `pynxtools` reader plugins install them alongside:

=== "uv"

    ```bash
    uv pip install pynxtools[xps] nomad-lab
    # or
    uv pip install pynxtools nomad-lab pynxtools-xps pynxtools-mpes
    ```

=== "pip"

    ```bash
    pip install pynxtools[xps] nomad-lab
    # or
    pip install pynxtools nomad-lab pynxtools-xps pynxtools-mpes
    ```

Verify that NOMAD recognizes the plugin:

```python
from nomad.config import config
print([p.name for p in config.plugins.entry_points])
# Should include pynxtools-related entries
```

---

## NOMAD OASIS — local deployment

NOMAD OASIS is a self-hosted deployment that gives institutions full control over
their data while retaining compatibility with the public NOMAD instance.

To include `pynxtools` in a NOMAD OASIS deployment, add it to the OASIS
optional dependencies in `pyproject.toml`:

```toml
[project.optional-dependencies]
plugins = [
 "pynxtools"
]
```

For OASIS setup details see the
[NOMAD OASIS documentation](https://nomad-lab.eu/prod/v1/docs/howto/oasis/install.html).

---

## Further reading

- [Tutorial → Uploading NeXus data to NOMAD](../../tutorial/nexus-to-nomad.md) —
  step-by-step guide to uploading a file via the GUI
- [How-tos → pynxtools → Use pynxtools with NOMAD](../../how-tos/pynxtools/use-with-nomad.md) —
  programmatic upload, OASIS setup, debugging parser output
- [NOMAD documentation](https://nomad-lab.eu/prod/v1/docs/)
- [NOMAD Metainfo browser](https://nomad-lab.eu/prod/v1/gui/analyze/metainfo/pynxtools)
