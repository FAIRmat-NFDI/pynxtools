# Validation of NeXus files in `pynxtools`

!!! info "This page is intended to give more information about the validation tools that are part of `pynxtools`. Please also have a look at our comprehensive [how-to guide](../../how-tos/pynxtools/validate-nexus-files.md) on NeXus validation."

The validity of NeXus files is fundamental to ensure FAIR data. Without specific requirements, it is not possible to understand the data. What type of experiment? What Laser Wavelength? Which voltage? What data is represented in a table? What is the unit of a value? Which ISO norm does this refer to? Where was this measured? Which year was this measured?

The NeXus application definitions define the minimum set of terms that must be reported for a given experiment (i.e., the required terms that you must add to the NeXus file in order to be compliant with that application definition). Application definitions may also define terms that are optional in the NeXus data file. NeXus files are considered valid if they comply with the respective NeXus application definition.

Oftentimes, there will be errors in generated NeXus files: Typos, missing required concepts, using the incorrect datatype or format (e.g., array instead of list, float instead of integer, etc.). Therefore, a validation is required, to ensure that the data you want to share is FAIR.

## Approach

One of the main advantages of using `pynxtools` is that it comes with its own validation tools. That is, it can be used to validate that a given NeXus/HDF5 file is compliant with a NeXus application definition.

The following use cases are covered by the validation in `pynxtools`:

- **Requirement concepts**: Warnings are logged if a required group/field/attribute is missing. This is also the case for required concepts within recommended/optional groups.
- **Namefitting**: NeXus allows for variable instance names for a given concept through the combination of uppercase notation and the `nameType` attribute (for more information see the [section on NeXus naming rules](../nexus/nexus-rules.md#name-resolution).) In the validation process, the name of any instance data is compared to the defined NeXus concepts. Errors are raised if a group/field uses a name defined for a concept of a different NeXus type (i.e., if a group in the instance data has the same name as a defined field). If a given instance data point cannot be fit to any concept, a warning is logged as well.
- **NeXus fields/attributes**:
    - For concepts where an [**enumeration**](https://manual.nexusformat.org/nxdl_desc.html#enumeration) is used, it is checked if the provided value is contained in the enumeration. For _closed_ enumerations, a warning is logged if the provided value does not match any of the enumeration choices. For _open_ enumerations, an info level message is logged in such cases.
    - Values of fields and attributes are checked against the [**NeXus data type**](https://manual.nexusformat.org/nxdl-types.html#index-0) and warnings are logged if a mismatch is detected.
    - Units for fields are validated using the Python units package [`pint`](https://pint.readthedocs.io/en/stable/) by confirming that the dimensionality of a given unit matches its [**NeXus Unit Category**](https://manual.nexusformat.org/nxdl-types.html#unit-categories-allowed-in-nxdl-specifications). Missing units and units for which no associated field is given also produce warning messages.
    - For NeXus attributes, a warning is logged if there is no associated group or field for the attribute.

- **`NXdata`**: The [**`NXdata`**](https://manual.nexusformat.org/classes/base_classes/NXdata.html#nxdata) group plays a special rule in NeXus as it is used to define [the plottable data](https://manual.nexusformat.org/examples/python/plotting/index.html) for an experiment. Therefore, it comes with a specific set of rules (especially the presence of the `@signal` and `@data`) attributes. The validator checks for the presence of these attributes and also ensures that the dimensionality of the signals and axes match.
- **Links**: When writing NeXus files in HDF5, any group or field can be replace by an [HDF5 link](https://manual.nexusformat.org/design.html#links) to another group/field. In the validation, these links are resolved and the validity of the resolved object against the NeXus definition is checked. In addition, the presence of the `@target` attribute (which is supposed to be set when using links) is checked.
- **Undocumented concepts**: In NeXus, it is allowed to add additional data that is not defined in the NeXus definitions (e.g., additional fields). In order to prevent unintended use of this feature (arising, for example, from misspelling of instance names), warnings are logged for any such additional data.
- **Reserved suffixes and prefixes**: NeXus defines a number of [reserved suffixes](https://manual.nexusformat.org/datarules.html#index-6). These are suffixes for the name of fields that can only be used if the actual field exists as well (e.g., the suffix `_set` in the field `temperature_set` would be used to report the setpoint for the field `temperature`). If the associated field does not exist, a warning is logged. In addition, NeXus also has a number of [reserved prefixes](https://manual.nexusformat.org/datarules.html#index-4), which can only be used in certain contexts (e.g., in a specific application definition). If such a prefix is used anywhere else, the validation tool produces a warning message.

## Validation use cases and tools

### As part of the dataconverter

During [data conversion](dataconverter-and-readers.md) within `pynxtools`, before writing the HDF5 file, the data is first checked against the provided application definition. In the conversion, we are using a [special combined notation](../nexus/nexus-primer.md#what-is-nexus) to indicate that instance paths shall match to NeXus concepts. As an example, the path `ENTRY[entry]/INSTRUMENT[instrument]/DETECTOR[detector]` indicates that we would like to create an HDf5 group at `/entry/instrument/detector` and that it shall match to the `NXdetector` group within `NXentry/NXinstrument`. While this notation makes it possible to connect instances to concepts in a succinct way, it also requires more rigorous check to validate that the names for instances and data actually match. Therefore, additional validation checks are implemented and warnings are logged if the two names have a mismatch.

It is also possible to define in the data conversion process whether the data shall be [compressed in the HDF5 file](https://docs.hdfgroup.org/archive/support/HDF5/faq/compression.html). Warnings are logged if the given compression strength (which must be between 0 and 9) is incorrect.

Since the validation is performed during the conversion, it is possible to automatically correct the data: as a convenience feature, any instance data that produces invalid files (e.g., when an HDF5 field would be named the same as a group in the NeXus definitions) are removed before writing the files. In addition, if a mismatch between the data type of the instance and the concept is detected, for we convert these values silently if possible (e.g., from int to float or from the string representation of bools (`"true"`/`"false"`) to actual booleans).

## validate_nexus: Validate existing NeXus/HDF5 files

While we encourage NeXus users to convert their data using the `pynxtools` data conversion pipeline, we also realize that a lot of NeXus files are created using other applications. For such use cases, `pynxtools` provides a **standalone validator** (called **`validate_nexus`**). This CLI tool can be used to validate _existing_ HDF5 files against the NeXus application definition they claim to be comply with. Read more in the [API documentation](../../reference/cli-api.md#validate_nexus).

Validation of existing files is generally more straightforward than validating the `pynxtools` template as the NeXus type (i.e., group/fields/attributes) of instance data is easily detected from the file structure. Therefore, no additional special rules are applied in `validate_nexus` other than those given above.

## read_nexus: NeXus file reader and debugger

In addition to the validation tools mentioned above, there is another utility in `pynxtools` called **`read_nexus`** (available from the command line after installation). This tool outputs a debug log for a given NeXus file by annotating the data and metadata entries with the schema definitions from the respective NeXus base classes and application definitions to which the file refers to. Read more in the [API documentation](../../reference/cli-api.md#nexus-file-validation).

<!-- ??? info "Using a different set of NeXus definitions"

    The environment variable "NEXUS_DEF_PATH" can be set to a directory which contains the NeXus definitions as NXDL XML files. If this environment variable is not defined, the module will use the definitions in its bundle (see `src/pynxtools/definitions`)._

    The environment variable can be set as follows:
    ```
    export 'NEXUS_DEF_PATH'=<folder_path_that_contains_nexus_defs>
    ``` -->

## Limitations

While we try to cover must NeXus use cases in the validation, there are some checks that we don't apply consistently yet. These limitations are mostly due to inconsistencies in the standard (like for the use of [symbols](https://manual.nexusformat.org/nxdl_desc.html#symbolstype) and dimensionalities) or because an idea in NeXus is seldomly used (like [NeXus choices](https://manual.nexusformat.org/nxdl_desc.html#choicetype)). We are looking forward to resolving such ambiguities with the NeXus community going forward, after which a more rigorous implementation in the validation software is possible.

## Other Validation software

There are several tools which can be used for validation of NeXus files.

1. [pynxtools](<https://github.com/FAIRmat-NFDI/pynxtools>) - our own software tool

2. [cnxvalidate: NeXus validation tool written in C](https://github.com/nexusformat/cnxvalidate)

3. [punx: Python Utilities for NeXus HDF5 files](https://github.com/prjemian/punx)

4. [nexpy/nxvalidate: A python API for validating NeXus file](https://github.com/nexpy/nxvalidate)

All are different and have individual advantages or disadvantages. We encourage users to have a look at the [how-to guide for these tools](../../how-tos/pynxtools/validate-nexus-files-other-tools.md) to learn more.
