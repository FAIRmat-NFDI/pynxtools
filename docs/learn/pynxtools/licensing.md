# Licensing

`pynxtools` is Apache-2.0 licensed. One part of the repository is an exception to that: the Python representation of the NeXus definitions generated for NOMAD (`src/pynxtools/nomad/metainfo/base_classes/` and `src/pynxtools/nomad/metainfo/applications/`) is licensed under **LGPL-3.0-or-later** instead.

## Reasoning

The NeXus definitions themselves (`src/pynxtools/definitions`, see [NeXus definitions in pynxtools](nexus-definitions.md)) are maintained upstream by the NeXus International Advisory Committee (NIAC) and distributed under LGPL-3.0-or-later.

`pynxtools` generates Python Metainfo classes from those NXDL definitions for use in NOMAD, see [pynxtools integration in NOMAD](nomad-integration.md) (see [NeXus metainfo generation](nexus-metainfo-generation.md)). The generator itself — the code that reads NXDL and produces Python source (`src/pynxtools/nomad/converters/`) — is our own, independent implementation, and stays Apache-2.0.

The *output* of that generator is a separate question. Although the generated `.py` files use a different representation than the original NXDL XML, they preserve the NXDL definitions' structure and content (class names, field names, cardinalities, documentation text, ...). That makes it unclear whether they should be treated as derivative works of the LGPL-licensed NXDL source — a question we haven't found a definitive answer to, and one a derivative-works analysis would need to settle conclusively.

To avoid this ambiguity, the generated files are licensed under LGPL-3.0-or-later, the same license as the NXDL definitions from which they are generated. The remainder of `pynxtools`, including the generator itself, remains licensed under Apache-2.0.

## What this means in practice

`pynxtools` contains files under two licenses:

- Most of the codebase, including the parsers, readers, and the generator itself, is licensed under Apache-2.0.
- The generated NeXus metainfo classes (`base_classes/` and `applications/`) are licensed under LGPL-3.0-or-later.

## How it's marked

We follow the [REUSE Software specification](https://reuse.software/) for this:

- Full license texts live in [`LICENSES/`](https://github.com/FAIRmat-NFDI/pynxtools/tree/main/LICENSES).
- Every file carries an `SPDX-License-Identifier` header stating the applicable license.
- Generated files additionally identify the originating NeXus definition and explain why they are licensed differently from the remainder of the package.

```python
# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXsample (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
```

<!-- TODO: add this clarifier when the whole repo is REUSE compliant.
You can check the whole repository's compliance with `pipx run reuse lint`. -->
