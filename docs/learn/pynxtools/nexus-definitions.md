# NeXus definitions in pynxtools

## Overview

`pynxtools` converts experimental data into the NeXus format and validates the resulting HDF5 files against NeXus application definitions. These definitions formally describe how experimental data and metadata must be structured in a NeXus file.

The NeXus definitions themselves are not part of the pynxtools source code. Instead, they are maintained in a dedicated repository and included in pynxtools as a Git submodule:

```bash
src/pynxtools/definitions
```

This page explains:

- what the definitions repository contains,

- why it is included as a submodule,

- how it is used inside `pynxtools`,

- and how to manage it using the provided helper script.

## What the NeXus definitions are

NeXus defines a standardized structure for scientific data. The structure is defined in XML files written in the NeXus Definition Language (NXDL). These XML files define:

- base classes (common structural components and respective semantic concepts),
- application definitions (experiment-specific schemas),
- contributed definitions from the community. These can be base classes or application definitions.

These definitions specify naming, hierarchy, constraints on the requiredness of individual concepts, and allowed metadata for NeXus files.

In practice, they serve as:

- the schema against which data is validated,
- the reference for generating templates and mappings,
- the source of truth for how experimental data must be organized.

Validation and interoperability depend directly on the exact version of these definitions.

!!! info "To learn more about the different versions of the NeXus definitions, see [Reference > NeXus definitions](../../reference/definitions.md)."

## Role of the definitions in `pynxtools`

`pynxtools` relies on a fixed, versioned set of NeXus definitions to ensure reproducibility and consistency across data conversions.

Specifically, the definitions are used to:

- generate internal representations of application definitions,
- validate generated NeXus files,
- ensure consistent interpretation of metadata across plugins,
- make conversions reproducible by tying results to a specific definitions version.

Because definitions evolve independently from `pynxtools`, the repository is included as a submodule rather than copied into the code base.

This has several advantages:

- updates can be performed independently of `pynxtools` releases,
- the exact definitions commit used for conversion is tracked,
- different branches or commits can be tested when developing new application definitions.

The version currently in use is written to `nexus-version.txt`, allowing downstream users or workflows to reconstruct which definitions were used.

## Why a Git submodule is used

The definitions repository is large and changes independently from the Python code. Using a submodule ensures that:

- Every `pynxtools` commit references an exact definitions commit.
- Users obtain reproducible behavior when cloning the repository.
- Developers can temporarily test newer or experimental definitions without changing the recorded version.

The superproject (`pynxtools`) therefore defines the authoritative version of the definitions.

## Managing the definitions submodule

The submodule should be managed through [a dedicated script](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/scripts/definitions.sh):

```bash
scripts/definitions.sh
```

The script provides a small abstraction over common Git submodule operations and ensures that:

- the correct definitions version is checked out,
- `.gitmodules` remains consistent,
- `nexus-version.txt` is updated automatically.

### Commands

- **Update to the tracked branch**:
  
    ```bash
    ./scripts/definitions.sh update
    ```

    Updates the definitions submodule to the latest commit of the tracked branch (if configured). Internally this runs: `git submodule update --remote`. Use this when you intentionally want to move to a newer definitions version.

- **Reset to the recorded version**:
  
    ```bash
    ./scripts/definitions.sh reset
    ```

    Resets the submodule to the exact commit recorded in the `pynxtools` repository.
    This is the safe operation when you want to switch branches, discard local experiments,
    or restore a clean state.

    Importantly, this does not update to the latest definitions version. It restores the version pinned by the current `pynxtools` commit.

- **Checkout a specific revision**:
  
    ```bash
    ./scripts/definitions.sh checkout <REV>
    ```
    
    `<REV>` can be any Git reference that is resolvable by `git rev-parse` (e.g., a commit hash, a tag, or a branch name).
    The behavior depends on the type:

    | Revision type | Result |
    |---|---|
    | commit or tag | submodule in detached HEAD |
    | branch | branch is checked out and tracked |
    
    If a branch is checked out, the script updates `.gitmodules` so that future update calls follow that branch. If a commit or tag is used, branch tracking is removed.

    This allows temporary testing of definitions changes without permanently modifying the repository state.

## Summary

The definitions submodule provides the schema layer that enables `pynxtools` to generate and validate NeXus-compliant data. By pinning a specific definitions commit, `pynxtools` guarantees reproducibility while still allowing developers to test newer or experimental definitions when required.

The helper script exists to make these operations explicit and safe, avoiding common pitfalls of manual submodule handling while keeping the underlying Git behavior transparent.