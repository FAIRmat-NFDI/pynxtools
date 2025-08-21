# Validation of NeXus files in `pynxtools`

!!! info "This page is intended to give more information about the validation tools that are part of `pynxtools`. Please also have a look at our comprehensive [how-to guide](../../how-tos/pynxtools/validate-nexus-files.md) on NeXus validation."

The validity of NeXus files is fundamental to ensure FAIR data. Without specific requirements, it is not possible to understand the data. What type of experiment? What Laser Wavelength? Which voltage? What data is represented in a table? What is the unit of a value? Which ISO norm does this refer to? Where was this measured? Which year was this measured?

The NeXus application definitions define the minimum set of terms that must be reported for a given experiment (i.e., the required terms that you must add to the NeXus file in order to be compliant with that application definition). Application definitions may also define terms that are optional in the NeXus data file. The requirements are set by the community _via_ workshops or at conferences.

Oftentimes, there will be errors in a generated NeXus file: Typos, missing required concepts, missing attributes, using the incorrect datatype or format (e.g., array instead of list, float instead of integer, etc.). Therefore, a validation is required, to ensure that the data you want to share is FAIR.

NeXus files are considered valid if they comply with the respective NeXus application definition.

One of the main advantages of using `pynxtools` is that it comes with its own validation tools. That is, it can be used to validate that a given NeXus/HDF5 file is compliant with a NeXus application definition.

## Approach

For the validation in `pynxtools`, we consider the following use cases:

- Requiredness: MissingRequiredGroup, MissingRequiredField, MissingRequiredAttribute
- Namefitting:
  - ExpectedGroup
  - ExpectedField
  - InvalidNexusTypeForNamedConcept
  - InvalidConceptForNonVariadic
  - KeysWithAndWithoutConcept
  - FailedNamefitting,  
- Validation of NeXus groups:
- Validation of NeXus fields/attributes:
  - Enumerations: InvalidEnum, OpenEnumWithNewItem
  - Data type:  InvalidType, InvalidDatetime, IsNotPosInt
  - Units: matching to the NeXus Unit Category, MissingUnit, UnitWithoutField
  - Attributes: AttributeForNonExistingConcept
- NXdata: NXdataMissingSignalData, NXdataMissingAxisData, NXdataAxisMismatch
- Links:  BrokenLink, MissingTargetAttribute, TargetAttributeMismatch
- Undocumented concepts: MissingDocumentation
- Reserved suffixes: ReservedSuffixWithoutField
- Reserved prefixes: ReservedPrefixInWrongContext 
- Compression: InvalidCompressionStrength, CompressionStrengthZero
    DifferentVariadicNodesWithTheSameName = auto()
    UnitWithoutDocumentation = auto()
    InvalidUnit = auto()

## Limitations

- Choice: ChoiceValidationError
- Symbols

## As part of the dataconverter

During [data conversion](./dataconverter-and-readers.md) within `pynxtools`, before writing the HDF5 file, the data is first checked against the provided application definition.

- Conversion of trivial types: str (true/false) to bool, int to float
- Removal of invalid keys: KeyToBeRemoved

## validate_nexus: Validate existing NeXus/HDF5 files

- MissingNXclass = auto()

While we encourage NeXus users to convert their data using the `pynxtools` data converter, we also realize that a lot of NeXus files are created using other applications. For such use cases, `pynxtools` provides a standalone validator (called `validate_nexus`). This CLI tool can be used to validate _existing_ HDF5 files against the NeXus application definition they claim to be comply with. Read more in the [API documentation](../../reference/cli-api.md#validate_nexus).

Validation of existing files is generally more straightforward than validating the `pynxtools` template. 

## read_nexus: NeXus file reader and debugger

This utility outputs a debug log for a given NeXus file by annotating the data and metadata entries with the schema definitions from the respective NeXus base classes and application definitions to which the file refers to. See [here](../../reference/cli-api.md#nexus-file-validation) for the API documentation.

If you have `pynxtools` installed, you can call the tool on the file mentioned above using the command

```bash
read_nexus 201805_WSe2_arpes.nxs
```

<!-- ??? info "Using a different set of NeXus definitions"

    The environment variable "NEXUS_DEF_PATH" can be set to a directory which contains the NeXus definitions as NXDL XML files. If this environment variable is not defined, the module will use the definitions in its bundle (see `src/pynxtools/definitions`)._

    The environment variable can be set as follows:
    ```
    export 'NEXUS_DEF_PATH'=<folder_path_that_contains_nexus_defs>
    ``` -->

??? info "A note to Windows users"

    If you run `read_nexus` from `git bash`, you need to set the environmental variable
    `MSYS_NO_PATHCONV` to avoid the [path translation in Windows Git MSys](https://stackoverflow.com/questions/7250130/how-to-stop-mingw-and-msys-from-mangling-path-names-given-at-the-command-line#34386471).
    The easiest way is to prefix the `read_nexus` call with `MSYS_NO_PATHCONV=1`:

    ```
    MSYS_NO_PATHCONV=1 read_nexus -c /NXarpes/ENTRY/INSTRUMENT/analyzer
    ```

    This workaround was tested with Windows 11, but should very likely also work with Windows 10 and lower.

## Other Validation software

There are several tools which can be used for validation of NeXus files. All are different and have individual advantages or disadvantages:

1. [pynxtools](<https://github.com/FAIRmat-NFDI/pynxtools>) - our own software tool

2. [cnxvalidate: NeXus validation tool written in C](https://github.com/nexusformat/cnxvalidate)

3. [punx: Python Utilities for NeXus HDF5 files](https://github.com/prjemian/punx)

4. [nexpy/nxvalidate: A python API for validating NeXus file](https://github.com/nexpy/nxvalidate)

??? info "A note on operating systems"
    Most of these tools were developed using Linux as operating system.
    If you are on Windows, some of them may not work or you will need additional
    installation steps than those documented. If you are used to Windows, consider setting up a Linux operating system to eliminate problems in the installation process and ensure compatibility.

We encourage users to have a look at the [how-to](../../how-tos/pynxtools/validate-nexus-files-other-tools.md) to learn more about these tools.