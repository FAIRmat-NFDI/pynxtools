# Writing your first application definition

This tutorial will guide you through writing your first valid NeXus application definition.

## What should you should know before this tutorial?

- You should have a basic understanding of NeXus: see [Learn > NeXus -> A primer on NeXus](../learn/nexus/nexus-primer.md)
- You should have `pynxtools` installed: see the [Installation guide](./installation.md)

!!! note
    For this tutorial, we will use the [`nyaml`](https://github.com/FAIRmat-NFDI/nyaml) tool (developed by FAIRmat) that lets you write the NXDL definition in YAML and convert it to NXDL XML.
    You can learn more in the [`nyaml` documentation](https://fairmat-nfdi.github.io/nyaml/).

## What you will know at the end of this tutorial?

You will know

- how to write a basic application definition
- how to validate the result with pynxtools
- how to add your new definition to `pynxtools`

You will understand

- the structure of NXDL files
- the role of base classes and application definitions
- NeXus naming rules
- optionality and dimensions in NXDL

---

## Goals

We want to build an application definition `NXdouble_slit` from scratch — a minimal but complete NeXus application definition for a classic optics experiment. 

---

## The experiment

In a [double-slit experiment](https://en.wikipedia.org/wiki/Double-slit_experiment) a coherent light source illuminates a barrier with two narrow slits. The diffracted waves interfere and produce a characteristic fringe pattern on a detector screen. Standard analysis extracts fringe spacing (→ wavelength) and envelope width (→ coherence length).

The data we need to record:

| Quantity | Why |
|----------|-----|
| Source wavelength | Determines fringe spacing |
| Slit width, slit separation | Determines diffraction envelope |
| Detector distance and pixel layout | Maps pixels to angles |
| 2D intensity array | The measurement itself |

---

## Steps



### 1. Start with the skeleton

Every application definition is an XML file following the NXDL schema. Create `NXdouble_slit.nxdl.xml` with the following minimal content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="nxdlformat.xsl"?>
<definition xmlns="http://definition.nexusformat.org/nxdl/3.1"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            category="application"
            type="group"
            name="NXdouble_slit"
            extends="NXobject"
            xsi:schemaLocation="http://definition.nexusformat.org/nxdl/3.1 ../nxdl.xsd">

    <doc>Application definition for a double-slit interference experiment.</doc>

    <group type="NXentry">

        <field name="definition">
            <enumeration><item value="NXdouble_slit"/></enumeration>
        </field>
        <field name="title"/>
        <field name="start_time" type="NX_DATE_TIME"/>

    </group>

</definition>
```

If you have `pynxtools` installed (see [Installation Guide](./installation.md)), add the NXDL XML file under `src/pynxtools/definitions/contributed_definitions` and validate that pynxtools can read it:

```bash
dataconverter generate-template --nxdl NXdouble_slit
```

You should see a JSON template listing paths like `/ENTRY[entry]/title` and `/ENTRY[entry]/start_time`.

!!! note "Concept paths vs. instance paths"
    The template uses *concept* names (`ENTRY`, `INSTRUMENT`) and *instance* names in brackets (`[entry]`). The bracketed name is the literal group name written to the HDF5 file; the upper-case name is the name of the NeXus concept. Read more in
    [Learn > ... > Rules for storing data in NeXus](../learn/nexus/nexus-rules.md).

The `definition` field with an `<enumeration>` is a convention — it locks the field to the name of the application definition so that readers and validators can identify the file format unambiguously.

#### Working with `nyaml`

From now on, you will exclusively develop this application definition in YAML. As outlined above, there exists a tool [`nyaml`](https://github.com/FAIRmat-NFDI/nyaml) (developed by FAIRmat) that lets you write the NXDL definition in YAML and convert it to NXDL XML.

Install the `nyaml` Python package:

=== "uv"

    ```bash
    uv pip install nyaml
    ```

=== "pip"

    Note that you will need to install the Python version manually beforehand.

    ```bash
    pip install --upgrade pip
    pip install nyaml
    ```

This installs a CLI command called `nyaml2nxdl` (or short `n2n`). Use this to convert your NXDL XML file to YAML:

```bash
nyaml2nxdl NXdouble_slit.nxdl.xml --output-file NXdouble_slit.yaml   # → 
```

Your basic application definition should look like this is the YAML format:

```yaml
category: application
doc: |
  Application definition for a double-slit interference experiment.
type: group
NXdouble_slit(NXobject):
  (NXentry):
    definition:
      enumeration: [NXdouble_slit]
    title:
    start_time(NX_DATE_TIME):
```

Now we can start adding components to the experiment model. Conceptually, the experiment will be structured roughly as follows:

```
NXentry
 ├─ NXinstrument
 │   ├─ NXsource
 │   ├─ NXslit
 │   └─ NXdetector
 │      └─ NXdata   (measurement data)
 └─ NXdata          (default plot)
```

`NXentry` represents a single measurement, `NXinstrument` describes the experimental setup, and `NXdata` defines the default plottable dataset.

---

### 2. Add the instrument

Nest the physical components inside `NXinstrument`. Start with the light source:

```yaml
    (NXinstrument):
      source(NXsource):
        wavelength(NX_FLOAT):
          unit: NX_WAVELENGTH
          doc: |
            Central wavelength of the light source.
```

!!! note "Unit categories"
    `unit: "NX_WAVELENGTH"` is a *unit category*, not a unit. It declares that the field stores a wavelength-equivalent quantity (nm, Å, µm, …). The actual unit chosen by the writer is stored as a sibling HDF5 attribute `wavelength/@units`. You should always try to use one of the existing unit categories (see [NeXus manual > Unit Categories](https://manual.nexusformat.org/nxdl-types.html#unit-categories-allowed-in-nxdl-specifications)). If none of these apply, you may use a raw string like `"eV/mm"` as an example. In this example, the instance units must match the dimension of energy over length.

---

### 3. Choose the right base class for the slit

Browse the base class catalogue in [NeXus manual > ... > Base classes](https://manual.nexusformat.org/classes/base_classes/index.html). You will find:

- `NXaperture` — generic aperture
- `NXslit` — specific to slit-type apertures, with `x_gap` and `y_gap` already defined

Always prefer the most specific class. Add it with an *instance name* that describes the physical object:

```yaml
      double_slit(NXslit):
        x_gap(NX_FLOAT):
          unit: NX_LENGTH
          doc: |
            Width of each individual slit.
        slit_separation(NX_FLOAT):
          unit: NX_LENGTH
          doc: |
            Center-to-center distance between the two slits.
        height(NX_FLOAT):
          unit: NX_LENGTH
          exists: optional
        material(NX_CHAR):
          exists: optional
```

!!! note "Instance name vs. concept name"
    `double_slit` is the *concept* name — the name of the concept as defined in the NeXus definitions. `NXslit` is the associated base class. By default (`nameType="specified"`) this exact literal string is required in every conforming HDF5 file. You can relax this with `nameType:"any"` to accept any valid name. See 
    [Learn > ... > Rules for storing data in NeXus > Name resolution](../learn/nexus/nexus-rules.md#name-resolution).

---

### 4. Add the detector with dimensions

The detector produces a 2D array. Use `<symbols>` to name the array dimensions and reference them in `<dimensions>`.

Add this block at the top, outside of the class `NXslit`:

```yaml
symbols:
  doc: |
    Dimension symbols used in this definition.
  n_x: |
    Number of detector pixels along x.
  n_y: |
    Number of detector pixels along y.
```

Using symbolic names (`n_x`, `n_y`) instead of hardcoded integers makes the definition self-documenting and allows validation tools to verify dimensional consistency across fields.

Then add the detector group inside `NXinstrument`:

```yaml
      detector(NXdetector):
        distance(NX_FLOAT):
          unit: NX_LENGTH
          doc: |
            Distance from the slit plane to the detector surface.
        data(NXdata):
          doc: |
            Raw 2D pixel data collected by the detector with no calibration
            applied. This group stores data at the lowest level of processing
            possible, indexed by integer pixel coordinates.
          \@signal:
            enumeration: [data]
          \@axes:
            enumeration: [['x', 'y']]
          data(NX_NUMBER):
            exists: recommended
            unit: NX_ANY
            doc: |
              Raw 2D intensity array indexed by pixel position.
            dimensions:
              rank: 2
              dim: (n_x, n_y)
          x(NX_INT):
            doc: |
              Pixel indices along the horizontal detector axis (0-based).
            dimensions:
              rank: 1
              dim: (n_x,)
          y(NX_INT):
            doc: |
              Pixel indices along the vertical detector axis (0-based).
            dimensions:
              rank: 1
              dim: (n_y,)
```

!!! note "Raw data first, processed data separately"
    Always store the rawest data you have. Here the detector axes are integer pixel indices (`x`, `y`), i.e., exactly what the hardware records. The calibrated  view with physical spatial offsets (mm, µm) belongs in a *separate* `NXdata`  group at the `NXentry` level, wired as the default plot (step 6 below). An optional `NXprocess` group can document the conversion between the two
    (step 5 below).

---

### 5. Add an optional processing group

Three levels express how important a concept is for conformance:

| Level | NXDL | nyaml | What validators do |
|-------|------|-------|------------|
| Required | `required="true"` | `required: true` | Fail/warn if absent |
| Recommended | `recommended="true"` | `recommended: true` | Warn if absent or accept |
| Optional | `optional="true"` | `optional: true` | Silently accept if absent |

Note that by default, every concept in a base class is optional (even if none of these keys is written), whereas in application definition, every concept is required, unless it is marked recommended or optional.

The pixel offsets above are recommended — essential for calibrated analysis but not always stored. Use `optional` for supplementary metadata like `material`.

!!! tip
    When in doubt, lean towards `recommended` over `required`. A definition that is too strict discourages adoption; a definition that is too loose loses its interoperability value.

#### Flexible naming with `nameType`

Names in both NXDL files and the files that instantiate the schema follow a particular naming logic. There's the possibility to define concept names that are _different_ to the names of the actual data instances. You can learn more about the naming rules in  [Learn > ... > Rules for storing data in NeXus](../learn/nexus/nexus-rules.md). In summary, NeXus names are defined by a combination of the `nameType` attribute and whether (parts of) the names are lower- or uppercase.

By default every named group, field, or attribute in NXDL requires an **exact** name in the HDF5 file (`nameType="specified"`). NeXus provides two relaxed alternatives:

| `nameType` | nyaml example | What it means |
|---|---|---|
| `specified` (default) | `double_slit(NXslit):` | Exactly the literal name `double_slit` |
| `any` | `(NXinstrument):` | Any valid HDF5 group name is accepted |
| `partial` | `processID(NXprocess):` | The `ID` suffix is a placeholder; any string can replace it |

The `(NXinstrument):` syntax (parentheses only, no name) that you already wrote is the `nameType="any"` shorthand — any instrument group name is valid.

`nameType="partial"` is useful when you expect **multiple concepts of the same type** but want to give each a meaningful name. The uppercase sequence `ID` marks the variable part; everything before it is the fixed prefix. For example, `processID` would match `processing_pixel_cal`, `processing01`, etc.

Add an optional processing group at the `(NXentry)` level (sibling of `(NXinstrument)`) to document how raw pixel data were converted to calibrated spatial offsets:

```yaml
    processID(NXprocess):
      nameType: partial
      exists: optional
      doc: |
        Describes one step in the processing chain that converts raw detector pixel data to the calibrated interference pattern stored in ``interference_pattern``. The 'ID' suffix in the group name is replaced by a short identifier chosen by the writer, e.g. 'pixel_calibration' or 'background_correction'. Multiple NXprocess groups may be present; their order is given by sequence_index.
      sequence_index(NX_INT):
        doc: |
          Sequence index of processing, for determining the order of multiple
          NXprocess steps. Starts with 1.
      description(NX_CHAR):
        doc: Free-text description of what this step does.
      program(NX_CHAR):
        exists: optional
        doc: Version string of the software.
      version(NX_CHAR):
        exists: optional
      date(NX_DATE_TIME):
        exists: optional
```

---

### 6. Wire up NXdata

`NXdata` marks the default plot. Tools like NOMAD use the `@signal` and `@axes` attributes to render data without requiring user configuration. Add it as a sibling of `NXinstrument` (and `processID`):

```yaml
    interference_pattern(NXdata):
      doc: |
        Default plot: the calibrated 2D interference pattern with spatial axes. The signal and axes may be linked to the raw detector arrays or derived from it via one or more NXprocess steps.
      \@signal:
        enumeration: [data]
      \@axes:
        enumeration: [['x_offset', 'y_offset']]
      data(NX_NUMBER):
        unit: NX_ANY
        doc: |
          2D interference intensity after any processing steps.
        dimensions:
          rank: 2
          dim: (n_x, n_y)
      x_offset(NX_FLOAT):
        unit: NX_LENGTH
        doc: |
          Horizontal spatial offset from the detector centre, derived from
          pixel index and pixel pitch.
        dimensions:
          rank: 1
          dim: (n_x,)
      y_offset(NX_FLOAT):
        unit: NX_LENGTH
        doc: |
          Vertical spatial offset from the detector centre, derived from
          pixel index and pixel pitch.
        dimensions:
          rank: 1
          dim: (n_y,)
```

The axes here are physical lengths (NX_LENGTH), not pixel indices — they represent where each pixel falls in real space after calibration.

!!! note
    In a real HDF5 file, `data` and the axis fields in `NXdata` could be HDF5 links pointing to the detector group — not duplicated data. The NXDL defines what *must be accessible* at that path; the writer decides whether to copy or link.

---

### 7. Validate

Now that we are done, we can convert back to NXDL XML:

```bash
nyaml2nxdl NXdouble_slit.yaml --output-file NXdouble_slit.nxdl.xml
```

Run `generate-template` one final time and check that all required paths are listed:

```bash
dataconverter generate-template --nxdl NXdouble_slit
```

Write a minimal HDF5 test file filling all required fields, then validate:

```bash
validate_nexus my_test_file.nxs
```

See [How-tos > pynxtools > Validate NeXus files](../how-tos/pynxtools/validate-nexus-files.md) for details on interpreting the output.

---

## The complete definition

You can find both `NXdouble_slit.yaml` and `NXdouble_slit.nxdl.xml` in the `pynxtools` examples:

- [`NXdouble_slit.yaml`](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/examples/custom-application-definition/NXdouble_slit.yaml)
- [`NXdouble_slit.nxdl.xml`](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/examples/custom-application-definition/NXdouble_slit.nxdl.xml)

??? success "NXdouble_slit.yaml (full)"
    ```yaml
    --8<-- "examples/custom-application-definition/NXdouble_slit.yaml"
    ```

??? success "NXdouble_slit.nxdl.xml (full)"
    ```xml
    --8<-- "examples/custom-application-definition/NXdouble_slit.nxdl.xml"
    ```

---

## Advanced: adding a new base class

In Nexus, you can not only compose existing base classes into application definitions, but also define your own base class. For this tutorial, we will create a new base class `NXlaser` that is a specialization of `NXsource`.

In our full application definition, we have an `NXsource` inside `NXinstrument`:

```yaml
NXdouble_slit(NXobject):
  (NXentry):
    (NXinstrument):
      source(NXsource):
        wavelength(NX_FLOAT):
          unit: NX_WAVELENGTH
          doc: |
            Central wavelength of the light source.
        coherence_length(NX_FLOAT):
          unit: NX_LENGTH
          exists: recommended
          doc: |
            Temporal coherence length of the source.
        type(NX_CHAR):
          exists: optional
          enumeration: [Laser]
```

Note that:
- the `wavelength` field is already defined in the [`NXsource` base class](http://manual.nexusformat.org/classes/base_classes/NXsource.html). We are just redefining its documentation
- we added here the `coherence_length` which is special for a laser, but not defined for all sources
- we narrowed down the possible values for the `type` field from all available options in `NXsource/type` to just "Laser". This specialization constrains the source to lasers.

All of this is possible and valid NXDL syntax. However, many experiments in NeXus may use lasers. In that case, it makes sense to specialize the `NXsource` class and create a new `NXlaser` base class.

Create a new YAML file called `NXlaser.yaml`:

```yaml
--8<-- "examples/custom-application-definition/NXlaser.yaml"
```

!!! note
    You do not need to redefine the units of the `wavelength` field here. In general, only those concepts that are either not defined in the inherited class or are overwritten shall be defined in the child class.

The complete `NXlaser.yaml` and `NXlaser.nxdl.xml` are in the `pynxtools` examples:

- [`NXlaser.yaml`](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/examples/custom-application-definition/NXlaser.yaml)
- [`NXlaser.nxdl.xml`](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/examples/custom-application-definition/NXlaser.nxdl.xml)

You can then use this new base class `NXlaser` in `NXdouble_slit`:

```yaml
NXdouble_slit(NXobject):
  (NXentry):
    (NXinstrument):
      source(NXlaser):
        wavelength(NX_FLOAT):
        coherence_length(NX_FLOAT):
          exists: recommended
```

Here, you only need to define whether any of the fields in `NXlaser` are required or recommended. All fields in base classes are optional; in the application definition, all of them are inherited. If we want to require or recommend any of them, we have to explicitly say so.


Convert both `NXlaser` and `NXdouble_slit` back to NXDL XML:

```bash
nyaml2nxdl NXlaser.yaml --output-file NXlaser.nxdl.xml
nyaml2nxdl NXdouble_slit.yaml --output-file NXdouble_slit.nxdl.xml
```

Because you now use the class `NXlaser`, you should see paths like `/ENTRY[entry]/LASER/wavelength` and `/ENTRY[entry]/LASER/coherence_length` in the generated JSON template.

---

## Add your definition to `pynxtools`

There are two paths depending on whether you want a local prototype or a community contribution.

### Option A — Local development (fastest)

Copy both NXDL files directly into the `contributed_definitions/` folder of your local `pynxtools` install or working tree:

```bash
cp NXlaser.nxdl.xml        src/pynxtools/definitions/contributed_definitions/
cp NXdouble_slit.nxdl.xml  src/pynxtools/definitions/contributed_definitions/
```

Verify that pynxtools picks them up:

```bash
dataconverter generate-template --nxdl NXdouble_slit
```

This change lives only in your local checkout. It is useful for iterating quickly before submitting upstream.

### Option B — Community contribution (permanent)

When your definition is stable, contribute it to the shared NeXus definitions repository so that all `pynxtools` users can benefit:

1. Fork [FAIRmat-NFDI/nexus_definitions](https://github.com/FAIRmat-NFDI/nexus_definitions) on GitHub.
2. Add your NXDL files under `contributed_definitions/` (new definitions) or `applications/` (promoted application definitions).
3. Open a pull request. The FAIRmat team will review the definition.
4. Once merged, update the `pynxtools` definitions submodule to bring the new definition in:

    ```bash
    # From the pynxtools repository root
    ./scripts/definitions.sh update
    ```

    This runs `git submodule update --remote` on the definitions submodule and records the new commit hash in pynxtools.

!!! note
    For very early-stage or instrument-specific definitions that are not yet ready for the community repository, Option A is the right choice. The `contributed_definitions/` path is scanned automatically by pynxtools — no code changes are needed.

### Option C — Standardization with the NIAC

When you use option B, your new definition will only be part of the FAIRmat NeXus definitions. Once your application definition or base class has gained sufficient approval from the community, it is possible to submit it to the NeXus International Advisory Committee (NIAC) for standardization. If approved, the new application definitions and base classes get eventually promoted to `applications/` or `base classes`, respectively.


## Next steps

- [How-tos > NeXus > Write an application definition (how-to)](../how-tos/nexus/write-an-application-definition.md) — quick reference for experienced users
- [Tutorial > Build a pynxtools reader](build-a-reader.md) — write a reader that produces files conforming to `NXdouble_slit`
- Contribute to [FAIRmat NeXus definitions](https://github.com/FAIRmat-NFDI/nexus_definitions)
