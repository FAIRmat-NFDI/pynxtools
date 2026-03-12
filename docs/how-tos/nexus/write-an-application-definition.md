# Write an application definition

An application definition is a formal contract specifying which fields and groups a NeXus file must, should, or may contain for a given experimental technique. Write one when no existing definition covers your measurement — consult the [NeXus definitions catalogue](https://fairmat-nfdi.github.io/nexus_definitions/) first.

For this how-to guide, we assume that you are familiar with:
- the NeXus data model — see [Learn > NeXus > A primer on NeXus](../../learn/nexus/nexus-primer.md)
- naming rules in NeXus — see [Learn > NeXus > # Rules for storing data in NeXus](../../learn/nexus/nexus-rules.md)

For a step-by-step walkthrough of the same material see the tutorial at [Tutorials > Writing your first application definition](../../tutorial/writing-an-application-definition.md).

---

## Step 1 — Design the data contract

Identify what information is needed for *standard measurements and analysis* in your field — nothing more, nothing less. Assign each piece an optionality level:

| Level | NXDL attribute | Meaning |
|-------|----------------|---------|
| Required | *(none)* | Validation fails if absent |
| Recommended | `recommended="true"` | Should be present; validation warns if absent |
| Optional | `optional="true"` | May be present; never causes a validation error |

**Example — double-slit interference experiment**

| Data | Level |
|------|-------|
| Source wavelength | Required |
| Slit width, slit separation | Required |
| Detector distance | Required |
| 2D intensity array + pixel axes | Required |
| Source coherence length | Recommended |
| Slit height, slit material | Optional |

---

## Step 2 — Map to NeXus base classes

Use the standard hierarchy and the most specific existing base class. Browse base classes at [fairmat-nfdi.github.io/nexus_definitions](https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/index.html).

```
/NXentry
  /NXinstrument
    /source (NXsource)              — light source
    /double_slit (NXslit)           — prefer NXslit over the generic NXaperture
    /detector (NXdetector)          — area detector
  /interference_pattern (NXdata)    — default plot
```
Use standard field names from the chosen base class where they exist
(`x_pixel_offset`, `y_pixel_offset` in `NXdetector`; `x_gap` in `NXslit`).

---

## Step 3 — Write the NXDL

Save as `NXdouble_slit.nxdl.xml`:

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

    <symbols> <!-- (1) -->
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

        <field name="definition"> <!-- (2) -->
            <enumeration><item value="NXdouble_slit"/></enumeration>
        </field>
        <field name="title"/>
        <field name="start_time" type="NX_DATE_TIME"> <!-- (3) -->
            <doc>ISO 8601 datetime. Include an explicit timezone.</doc>
        </field>
        <field name="end_time" type="NX_DATE_TIME" recommended="true"/>

        <group type="NXinstrument">

            <group name="source" type="NXsource">
                <field name="wavelength" type="NX_FLOAT" units="NX_WAVELENGTH"> <!-- (4) -->
                    <doc>Central wavelength of the light source.</doc>
                </field>
                <field name="coherence_length" type="NX_FLOAT" units="NX_LENGTH"
                       recommended="true"> <!-- (5) -->
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

            <group name="double_slit" type="NXslit"> <!-- (6) -->
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
                    <dimensions rank="2"> <!-- (7) -->
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

        <group name="interference_pattern" type="NXdata"> <!-- (8) -->
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

Key patterns:

1. **`<symbols>`** — named dimension constants; reference them in `<dim value="..."/>` instead of
   hardcoding integers.
2. **`definition` field with `<enumeration>`** — locks the field to the appdef name; required by
   modern convention.
3. **NeXus types** — always specify `type="NX_DATE_TIME"`, `type="NX_FLOAT"`, etc. The default is
   `NX_CHAR`.
4. **Unit categories** — use `NX_WAVELENGTH`, `NX_LENGTH`, `NX_ENERGY`, etc., *not* raw strings
   like `"m"`. Full list in the
   [NeXus units reference](https://manual.nexusformat.org/nxdl-types.html#unit-categories).
5. **Optionality** — no attribute = required; `recommended="true"` = soft requirement;
   `optional="true"` = free.
6. **Instance vs. concept name** — `name="double_slit"` is the *instance* name written to the HDF5
   file; `type="NXslit"` is the *concept*. See [naming rules](../../learn/nexus/nexus-rules.md).
7. **`<dimensions>`** — rank and `dim` values must be consistent. Use symbolic names from
   `<symbols>`.
8. **`NXdata`** — always include a default-plot group with `@signal` and `@axes` attributes. In a
   real HDF5 file these fields would typically be hard links into the detector group.

### Alternative: write in YAML with nyaml

The [`nyaml`](https://github.com/FAIRmat-NFDI/nyaml) tool (developed by FAIRmat) lets you write the same definition in YAML and convert it to NXDL XML:

```bash
pip install nyaml
nyaml2nxdl NXdouble_slit.yaml   # → NXdouble_slit.nxdl.xml
```

The YAML syntax maps one-to-one to the XML: groups become keys, fields become nested keys with
`type`/`unit`/`doc` sub-keys, and attributes use the `\@`-prefix.

You can learn more in the [`nyaml` documentation](https://fairmat-nfdi.github.io/nyaml/).

---

## Step 4 — Validate locally

Place the file in `src/pynxtools/definitions/contributed_definitions/` and run:

```bash
dataconverter generate-template --nxdl NXdouble_slit
```

This confirms `pynxtools` resolves the definition and lists all expected paths.

!!! note
    The `dataconverter generate-template` method does not actually validate the NeXus definition
    by itself. Rather, it creates a `pynxtools` Template from a given application definition. 
    For this to work, the application definition has to be valid.

    Note that there exist a [validation workflow](https://github.com/FAIRmat-NFDI/nexus_definitions/blob/fairmat/.github/workflows/validate.yaml) that is run in the GitHub CI/CD of the definitions repository. For this to run on your NXDL file, you need to add your application definition there (see below).

---

## Step 5 — Contribute

Submit to the [FAIRmat NeXus definitions repository](https://github.com/FAIRmat-NFDI/nexus_definitions) — new classes go in `contributed_definitions/`. Open a pull request and the FAIRmat team will review it. Once the application definition or base class has gained sufficient from the community, it is possible to submit it to the NeXus International Advisory Committee for review. If approved, the new application definitions and base classes get eventually promoted to `applications/` or `base classes`, respectively.

To gather feedback before submitting, use the [hypothes.is](https://hypothes.is/) annotation tool on the [FAIRmat NeXus definitions site](https://fairmat-nfdi.github.io/nexus_definitions/).
