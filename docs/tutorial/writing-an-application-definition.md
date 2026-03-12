# Write your first application definition

This tutorial will guide you through on how to write your first valid NeXus application definition.

## What should you should know before this tutorial?

- You should have a basic understanding of NeXus: see [Learn > NeXus -> A primer on NeXus](../learn/nexus/nexus-primer.md)
- You should have `pynxtools` installed: see the [Installation guide](./installation.md)

## What you will know at the end of this tutorial?

You will know

- how to write a basic application definition
- how to validate the result with pynxtools.
- how to add your new definition to `pynxtools`

You will understand

- the structure of NXDL files
- the role of base classes and application definitions
- NeXus naming rules
- optionality and dimensions in NXDL

---

## Goals

We want to build an application definition `NXdouble_slit` from scratch — a minimal but complete NeXus application definition for a classic optics experiment. 


## 0. The experiment

In a [double-slit experiment](https://en.wikipedia.org/wiki/Double-slit_experiment) a coherent light source illuminates a barrier with two narrow slits. The diffracted waves interfere and produce a characteristic fringe pattern on a detector screen. Standard analysis extracts fringe spacing (→ wavelength) and envelope width (→ coherence length).

The data we need to record:

| Quantity | Why |
|----------|-----|
| Source wavelength | Determines fringe spacing |
| Slit width, slit separation | Determines diffraction envelope |
| Detector distance and pixel layout | Maps pixels to angles |
| 2D intensity array | The measurement itself |

---

## 1. Start with the skeleton

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
    The template uses *concept* names in upper case (`ENTRY`, `INSTRUMENT`) and *instance* names
    in brackets (`[entry]`). The bracketed name is the literal group name written to the HDF5 file;
    the upper-case name is the NeXus base class. Read more in
    [Learn > ... > Rules for storing data in NeXus](../learn/nexus/nexus-rules.md).

The `definition` field with an `<enumeration>` is a convention — it locks the field to the name of the application definition so that readers and validators can identify the file format unambiguously.

---

## 2. Add the instrument

Nest the physical components inside `NXinstrument`. Start with the light source:

```xml
        <group type="NXinstrument">

            <group name="source" type="NXsource">
                <field name="wavelength" type="NX_FLOAT" units="NX_WAVELENGTH">
                    <doc>Central wavelength of the light source.</doc>
                </field>
            </group>

        </group>
```

Run `generate-template` again — you will see
`/ENTRY[entry]/INSTRUMENT[instrument]/source/wavelength` appear.

!!! note "Unit categories"
    `units="NX_WAVELENGTH"` is a *unit category*, not a unit. It declares that the field stores a wavelength-equivalent quantity (nm, Å, µm, …). The actual unit chosen by the writer is stored as a sibling HDF5 attribute `wavelength/@units`. You should always try to use one of the existing unit categories (see [NeXus manual > Unit Categories](https://manual.nexusformat.org/nxdl-types.html#unit-categories-allowed-in-nxdl-specifications). If none of these apply, you may use a raw string like `"eV/mm"` as an example. In this example, the instance units must match the dimension of energy over length.
    ).

---

## 3. Choose the right base class for the slit

Browse the base class catalogue in [NeXus manual > ... > Base classes](https://manual.nexusformat.org/classes/base_classes/index.html). You will find:

- `NXaperture` — generic aperture
- `NXslit` — specific to slit-type apertures, with `x_gap` and `y_gap` already defined

Always prefer the most specific class. Add it with an *instance name* that describes the physical object:

```xml
            <group name="double_slit" type="NXslit">
                <field name="x_gap" type="NX_FLOAT" units="NX_LENGTH">
                    <doc>Width of each individual slit.</doc>
                </field>
                <field name="slit_separation" type="NX_FLOAT" units="NX_LENGTH">
                    <doc>Center-to-center distance between the two slits.</doc>
                </field>
                <field name="material" type="NX_CHAR" optional="true"/>
            </group>
```

!!! note "Instance name vs. concept name"
    `name="double_slit"` is the *concept* name — the name of the concept as defined in the NeXus definitions `type="NXslit"` is the associated base class  — the base class. By default (`nameType="specified"`) this exact string is required in every conforming file. You can relax this with `nameType="any"` to accept any valid name. See 
    [Learn > ... > Rules for storing data in NeXus > Name resolution](../learn/nexus/nexus-rules.md#name-resolutin).

 literal string written to the HDF5 group.

---

## 4. Add the detector with dimensions

The detector produces a 2D array. Use `<symbols>` to name the array dimensions and reference them in `<dimensions>`.

Add this block at the top of `<definition>`, before `<doc>`:

```xml
    <symbols>
        <doc>Dimension symbols used in this definition.</doc>
        <symbol name="n_x"><doc>Number of detector pixels along x.</doc></symbol>
        <symbol name="n_y"><doc>Number of detector pixels along y.</doc></symbol>
    </symbols>
```

Then add the detector group inside `NXinstrument`:

```xml
            <group name="detector" type="NXdetector">
                <field name="distance" type="NX_FLOAT" units="NX_LENGTH">
                    <doc>Distance from the slit plane to the detector surface.</doc>
                </field>
                <field name="data" type="NX_NUMBER" units="NX_ANY">
                    <doc>Measured 2D interference intensity pattern.</doc>
                    <dimensions rank="2">
                        <dim index="1" value="n_y"/>
                        <dim index="2" value="n_x"/>
                    </dimensions>
                </field>
                <field name="x_pixel_offset" type="NX_FLOAT" units="NX_LENGTH"
                       recommended="true">
                    <doc>Horizontal pixel positions relative to the detector centre.</doc>
                    <dimensions rank="1"><dim index="1" value="n_x"/></dimensions>
                </field>
                <field name="y_pixel_offset" type="NX_FLOAT" units="NX_LENGTH"
                       recommended="true">
                    <doc>Vertical pixel positions relative to the detector centre.</doc>
                    <dimensions rank="1"><dim index="1" value="n_y"/></dimensions>
                </field>
            </group>
```

Using symbolic names (`n_x`, `n_y`) instead of hardcoded integers makes the definition self-documenting and allows validation tools to verify dimensional consistency across fields.

---

## 5. Optionality levels

Three levels express how important a field is for conformance:

| Level | NXDL | What validators do |
|-------|------|--------------------|
| Required | `required="true"`  | Fail if absent |
| Recommended | `recommended="true"` | Warn if absent |
| Optional | `optional="true"` | Silently accept if absent |

Note that by default, every concept in a base class is optional (even if none of these keys is written), whereas in application definition, every concept is required by default.

The pixel offsets above are `recommended="true"` — essential for calibrated analysis but not always stored. Use `optional="true"` for supplementary metadata like `material`.

!!! tip
    When in doubt, lean towards `recommended` over `required`. A definition that is too strict discourages adoption; a definition that is too loose loses its interoperability value.

---

## 6. Wire up NXdata

`NXdata` marks the default plot. Tools like NOMAD use the `@signal` and `@axes` attributes to
render data without requiring user configuration. Add it as a sibling of `NXinstrument`:

```xml
        <group name="interference_pattern" type="NXdata">
            <doc>Default plot: the 2D interference pattern.</doc>
            <attribute name="signal" value="data"/>
            <attribute name="axes" value="y_pixel_offset x_pixel_offset"/>
            <field name="data" type="NX_NUMBER" units="NX_ANY">
                <dimensions rank="2">
                    <dim index="1" value="n_y"/>
                    <dim index="2" value="n_x"/>
                </dimensions>
            </field>
            <field name="x_pixel_offset" type="NX_FLOAT" units="NX_LENGTH">
                <dimensions rank="1"><dim index="1" value="n_x"/></dimensions>
            </field>
            <field name="y_pixel_offset" type="NX_FLOAT" units="NX_LENGTH">
                <dimensions rank="1"><dim index="1" value="n_y"/></dimensions>
            </field>
        </group>
```

!!! note
    In a real HDF5 file, `data` and the axis fields in `NXdata` are typically HDF5 hard links
    pointing to the detector group — not duplicated data. The NXDL defines what *must be
    accessible* at that path; the writer decides whether to copy or link.

---

## 7. Validate

Run `generate-template` one final time and check that all required paths are listed:

```bash
dataconverter generate-template --nxdl NXdouble_slit
```

Write a minimal HDF5 test file filling all required fields, then validate:

```bash
read_nexus my_test_file.nxs
```

See [Validate NeXus files](../how-tos/pynxtools/validate-nexus-files.md) for details on
interpreting the output.

---

## The complete definition

??? success "NXdouble_slit.nxdl.xml (full)"

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

        <symbols>
            <doc>Dimension symbols used in this definition.</doc>
            <symbol name="n_x"><doc>Number of detector pixels along x.</doc></symbol>
            <symbol name="n_y"><doc>Number of detector pixels along y.</doc></symbol>
        </symbols>

        <doc>
            Application definition for a double-slit interference experiment.
            Records the light source, aperture geometry, detector layout, and the
            measured 2D interference pattern needed to determine fringe spacing and
            source coherence length.

            See https://en.wikipedia.org/wiki/Double-slit_experiment.
        </doc>

        <group type="NXentry">

            <field name="definition">
                <enumeration><item value="NXdouble_slit"/></enumeration>
            </field>
            <field name="title"/>
            <field name="start_time" type="NX_DATE_TIME">
                <doc>ISO 8601 datetime. Include an explicit timezone.</doc>
            </field>
            <field name="end_time" type="NX_DATE_TIME" recommended="true"/>

            <group type="NXinstrument">

                <group name="source" type="NXsource">
                    <field name="wavelength" type="NX_FLOAT" units="NX_WAVELENGTH">
                        <doc>Central wavelength of the light source.</doc>
                    </field>
                    <field name="coherence_length" type="NX_FLOAT" units="NX_LENGTH"
                           recommended="true">
                        <doc>Temporal coherence length of the source.</doc>
                    </field>
                    <field name="type" type="NX_CHAR" optional="true">
                        <enumeration>
                            <item value="Laser"/>
                            <item value="Filtered lamp"/>
                            <item value="LED"/>
                        </enumeration>
                    </field>
                </group>

                <group name="double_slit" type="NXslit">
                    <field name="x_gap" type="NX_FLOAT" units="NX_LENGTH">
                        <doc>Width of each individual slit.</doc>
                    </field>
                    <field name="slit_separation" type="NX_FLOAT" units="NX_LENGTH">
                        <doc>Center-to-center distance between the two slits.</doc>
                    </field>
                    <field name="height" type="NX_FLOAT" units="NX_LENGTH" optional="true"/>
                    <field name="material" type="NX_CHAR" optional="true"/>
                </group>

                <group name="detector" type="NXdetector">
                    <field name="distance" type="NX_FLOAT" units="NX_LENGTH">
                        <doc>Distance from the slit plane to the detector surface.</doc>
                    </field>
                    <field name="data" type="NX_NUMBER" units="NX_ANY">
                        <doc>Measured 2D interference intensity pattern.</doc>
                        <dimensions rank="2">
                            <dim index="1" value="n_y"/>
                            <dim index="2" value="n_x"/>
                        </dimensions>
                    </field>
                    <field name="x_pixel_offset" type="NX_FLOAT" units="NX_LENGTH"
                           recommended="true">
                        <doc>Horizontal pixel positions relative to the detector centre.</doc>
                        <dimensions rank="1"><dim index="1" value="n_x"/></dimensions>
                    </field>
                    <field name="y_pixel_offset" type="NX_FLOAT" units="NX_LENGTH"
                           recommended="true">
                        <doc>Vertical pixel positions relative to the detector centre.</doc>
                        <dimensions rank="1"><dim index="1" value="n_y"/></dimensions>
                    </field>
                </group>

            </group>

            <group name="interference_pattern" type="NXdata">
                <doc>Default plot: the recorded 2D interference pattern.</doc>
                <attribute name="signal" value="data"/>
                <attribute name="axes" value="y_pixel_offset x_pixel_offset"/>
                <field name="data" type="NX_NUMBER" units="NX_ANY">
                    <dimensions rank="2">
                        <dim index="1" value="n_y"/>
                        <dim index="2" value="n_x"/>
                    </dimensions>
                </field>
                <field name="x_pixel_offset" type="NX_FLOAT" units="NX_LENGTH">
                    <dimensions rank="1"><dim index="1" value="n_x"/></dimensions>
                </field>
                <field name="y_pixel_offset" type="NX_FLOAT" units="NX_LENGTH">
                    <dimensions rank="1"><dim index="1" value="n_y"/></dimensions>
                </field>
            </group>

        </group>

    </definition>
    ```

---

## Next steps

- [Write an application definition (how-to)](../how-tos/nexus/writing-an-application-definition.md) — quick reference for experienced users
- [Build a pynxtools reader](build-a-reader.md) — write a reader that produces files conforming to `NXdouble_slit`
- Contribute to [FAIRmat NeXus definitions](https://github.com/FAIRmat-NFDI/nexus_definitions)
