# Validation of NeXus files using external software

!!! info "This is a how-to guide for using different tools to validate NeXus files. If you want to learn more about how validation is done in `pynxtools`, please visit the [explanation](../../learn/pynxtools/nexus-validation.md) or [how-to](../../learn/pynxtools/nexus-validation.md) pages."

??? danger "This part of the documentation is talking about external tools (i.e., not tools not maintained by FAIRmat) that are subject to change. If these tools do change, you may find outdated information here. We do not take any responsibility for these software tools and for any issues arising from installation/usage."

In this how-to guide, we will learn how to use different software tools to validate existing NeXus files. Specifically, we want to use tools to validate NeXus files against a given set of NeXus definitions. This can be the official version of the NeXus definitions or a different version used for local development. Here, we will work with two different versions of the definitions.

  1. [Definitions standardized by the NeXus International Advisory Committee (NIAC)](https://manual.nexusformat.org/)

  2. [FAIRmat NeXus proposal](https://fairmat-nfdi.github.io/nexus_definitions/index.html#)

!!! info "Dataset"
    You can download the dataset used in this how-to guide here:

    [201805_WSe2_arpes.nxs](https://raw.githubusercontent.com/FAIRmat-NFDI/pynxtools/master/src/pynxtools/data/201805_WSe2_arpes.nxs){:target="_blank" .md-button }

    This is an angular-resolved photoelectron spectroscopy (ARPES) dataset that is formatted according to the [`NXarpes`](https://manual.nexusformat.org/classes/applications/NXarpes.html#nxarpes) application definition.

## Software tools

Aside from the tools we develop within FAIRmat, the [official NeXus website](https://manual.nexusformat.org/validation.html) lists additional programs for the validation of NeXus files:

1. [`cnxvalidate`](https://github.com/nexusformat/cnxvalidate): NeXus validation tool written in C
2. [`punx`](https://github.com/prjemian/punx): Python Utilities for NeXus HDF5 files
3. [`nexpy/nxvalidate`](https://github.com/nexpy/nxvalidate): A Python API for validating NeXus file

In case you are interested in testing these tools, we encourage you to follow these links to understand the details of these programs.

## `cnxvalidate`

`cnxvalidate` is the validation tool that the NeXus International Advisory Committee (NIAC) has been developing and recommending to external users.

- [Github Repository](<https://github.com/nexusformat/cnxvalidate>)

### Installation

??? info "A note on operating systems"
    Note that installation on Windows can be tricky because cmake can sometimes not find the libxml2 library. Though, if you solve this, this may work on Windows. Therefore, we recommend to use Linux.

The tool `cnxvalidate` is written in C and has to be built from source (e.g., by using `cmake`).

#### Install `cmake`, `HDF5` & `xml2` libraries

Install all dependencies required to install `cnxvalidate` via `cmake`:

```console
sudo apt-get update
sudo apt-get install git
sudo apt-get install build-essential
sudo add-apt-repository universe
sudo apt-get install libhdf5-serial-dev
sudo apt-get -y install pkg-config     
sudo apt upgrade -y
sudo apt-get -y install cmake
sudo apt-get install libxml2-dev
```

#### Clone the Github repository

Clone the GitHub repository:

```console
git clone https://github.com/nexusformat/cnxvalidate.git
```

Enter the cloned repository via the command

```console
cd cnxvalidate
```

Create a new directory called `build` and enter it:

```console
mkdir -p build && cd build
```

Use `cmake` to configure and compile all functionalities of the software, especially external libraries such as the `xml2` and `hdf5` libraries.

```console
cmake ../
```

Install `cnxvalidate` after it was successfully build

```console
cd build
make
```

Now, the executable is located at:

```console
/.../cnxvalidate/build/nxvalidate
```

You will also need to have a local copy of the NeXus definitions that you can point `cnxvalidate` to with the `-l` option.


!!! info "Getting the NeXus definitions"
    Download a set of NeXus definitions (choose only one).

    For the NIAC NeXus definitions:

    ```console
    git clone https://github.com/nexusformat/definitions.git
    ```

    For the FAIRmat NeXus definitions, clone the repository:

    ```console
    git clone https://github.com/FAIRmat-NFDI/nexus_definitions.git definitions/
    ```

    Now you have a folder called "definitions". The path to this definitions folder is used in the `-l` option of `cnxvalidate` to tell the program which NeXus definitions shall be used.

### Usage

After installation, you can invoke the help call from the command line:

=== "Source"
    ```console
    nxvalidate --help
    ```

=== "Result"
    ```console
    Usage:
        nxvvalidate -a appdef -l appdefdir -p pathtovalidate -o -b -u -d -t -r datafile
    -e Neaten output with more whitespace
    -t Produce all output possible
    -d Produce debug output tracing what nxvalidate does
    -b Warn about additional elements in the data file found in a base class
    -u Warn about undefined additional elements in the data file
    -o Warn about optional elements which are not present in the datafile
    -r Process the root group
    -x Check the depends_on chain for every dataset with the depends_on attribute
    ```

### Validation in `cnxvalidate`

Now you can use `cnxvalidate` with the executable called `nxvalidate` to validate the NeXus file called `FILE` (using the set of NeXus definitions in `DEFINITIONS`):

```console
nxvalidate -l DEFINITIONS FILE
```

You can now invoke the validation on the test file:

=== "Source"
    ```console
    ./nxvalidate -l definitions 201805_WSe2_arpes.nxs
    ```

=== "Result"
    ```console
    definition=NXarpes.nxdl.xml message="Required units attribute missing" nxdlPath=/NXentry/NXinstrument/NXdetector/entrance_slit_setting sev=error dataPath=/entry/instrument/analyser/entrance_slit_setting dataFile=201805_WSe2_arpes.nxs
    1 errors and 57 warnings found when validating 201805_WSe2_arpes.nxs
    ```

The output messages tell you now which groups/fields/attributes (message: "Required group/field/attribute missing") or units are missing (message: "Required units attribute missing), and so on.

## `punx` - Python Utilities for NeXus HDF5 files

Next up, we are testing `punx`, a Python package for working with NeXus HDF5 files.

### Installation

The package can be installed via any Python package manager:

=== "uv"
    ```console
    uv pip install punx
    ```

=== "pip"

    ```console
    pip install punx
    ```

You then need to setup the software. This requires installing the NeXus definitions into the local cache and downloading some demonstration files:

=== "Source"
    ```console
    punx install
    ```

=== "Result"
    ```console
    !!! WARNING: this program is not ready for distribution.

    [INFO 2025-08-21 14:03:52.011 punx.main:253] cache_manager.download_file_set('main', '/home/user/.config/punx', force=False)
    Downloading file set: main to /home/user/.config/punx/main ...
    Requesting download from https://github.com/nexusformat/definitions/archive/main.zip
    1 Extracted: definitions-main/applications/NXapm.nxdl.xml
    2 Extracted: definitions-main/applications/NXarchive.nxdl.xml
    3 Extracted: definitions-main/applications/NXarpes.nxdl.xml
    4 Extracted: definitions-main/applications/NXcanSAS.nxdl.xml
    5 Extracted: definitions-main/applications/NXdirecttof.nxdl.xml
    6 Extracted: definitions-main/applications/NXellipsometry.nxdl.xml
    7 Extracted: definitions-main/applications/NXfluo.nxdl.xml
    8 Extracted: definitions-main/applications/NXindirecttof.nxdl.xml
    9 Extracted: definitions-main/applications/NXiqproc.nxdl.xml
    10 Extracted: definitions-main/applications/NXlauetof.nxdl.xml
    11 Extracted: definitions-main/applications/NXmonopd.nxdl.xml
    12 Extracted: definitions-main/applications/NXmpes.nxdl.xml
    13 Extracted: definitions-main/applications/NXmpes_arpes.nxdl.xml
    14 Extracted: definitions-main/applications/NXmx.nxdl.xml
    15 Extracted: definitions-main/applications/NXoptical_spectroscopy.nxdl.xml
    16 Extracted: definitions-main/applications/NXraman.nxdl.xml
    17 Extracted: definitions-main/applications/NXrefscan.nxdl.xml
    18 Extracted: definitions-main/applications/NXreftof.nxdl.xml
    19 Extracted: definitions-main/applications/NXsas.nxdl.xml
    20 Extracted: definitions-main/applications/NXsastof.nxdl.xml
    21 Extracted: definitions-main/applications/NXscan.nxdl.xml
    22 Extracted: definitions-main/applications/NXspe.nxdl.xml
    23 Extracted: definitions-main/applications/NXsqom.nxdl.xml
    24 Extracted: definitions-main/applications/NXstxm.nxdl.xml
    25 Extracted: definitions-main/applications/NXtas.nxdl.xml
    26 Extracted: definitions-main/applications/NXtofnpd.nxdl.xml
    27 Extracted: definitions-main/applications/NXtofraw.nxdl.xml
    28 Extracted: definitions-main/applications/NXtofsingle.nxdl.xml
    29 Extracted: definitions-main/applications/NXtomo.nxdl.xml
    30 Extracted: definitions-main/applications/NXtomophase.nxdl.xml
    31 Extracted: definitions-main/applications/NXtomoproc.nxdl.xml
    32 Extracted: definitions-main/applications/NXxas.nxdl.xml
    33 Extracted: definitions-main/applications/NXxasproc.nxdl.xml
    34 Extracted: definitions-main/applications/NXxbase.nxdl.xml
    35 Extracted: definitions-main/applications/NXxeuler.nxdl.xml
    36 Extracted: definitions-main/applications/NXxkappa.nxdl.xml
    37 Extracted: definitions-main/applications/NXxlaue.nxdl.xml
    38 Extracted: definitions-main/applications/NXxlaueplate.nxdl.xml
    39 Extracted: definitions-main/applications/NXxnb.nxdl.xml
    40 Extracted: definitions-main/applications/NXxps.nxdl.xml
    41 Extracted: definitions-main/applications/NXxrot.nxdl.xml
    42 Extracted: definitions-main/applications/nxdlformat.xsl
    43 Extracted: definitions-main/base_classes/NXactivity.nxdl.xml
    44 Extracted: definitions-main/base_classes/NXactuator.nxdl.xml
    45 Extracted: definitions-main/base_classes/NXaperture.nxdl.xml
    46 Extracted: definitions-main/base_classes/NXapm_charge_state_analysis.nxdl.xml
    47 Extracted: definitions-main/base_classes/NXapm_measurement.nxdl.xml
    48 Extracted: definitions-main/base_classes/NXapm_ranging.nxdl.xml
    49 Extracted: definitions-main/base_classes/NXapm_reconstruction.nxdl.xml
    50 Extracted: definitions-main/base_classes/NXapm_simulation.nxdl.xml
    51 Extracted: definitions-main/base_classes/NXatom.nxdl.xml
    52 Extracted: definitions-main/base_classes/NXattenuator.nxdl.xml
    53 Extracted: definitions-main/base_classes/NXbeam.nxdl.xml
    54 Extracted: definitions-main/base_classes/NXbeam_stop.nxdl.xml
    55 Extracted: definitions-main/base_classes/NXbeam_transfer_matrix_table.nxdl.xml
    56 Extracted: definitions-main/base_classes/NXbending_magnet.nxdl.xml
    57 Extracted: definitions-main/base_classes/NXcalibration.nxdl.xml
    58 Extracted: definitions-main/base_classes/NXcapillary.nxdl.xml
    59 Extracted: definitions-main/base_classes/NXcg_alpha_complex.nxdl.xml
    60 Extracted: definitions-main/base_classes/NXcg_cylinder.nxdl.xml
    61 Extracted: definitions-main/base_classes/NXcg_ellipsoid.nxdl.xml
    62 Extracted: definitions-main/base_classes/NXcg_face_list_data_structure.nxdl.xml
    63 Extracted: definitions-main/base_classes/NXcg_grid.nxdl.xml
    64 Extracted: definitions-main/base_classes/NXcg_half_edge_data_structure.nxdl.xml
    65 Extracted: definitions-main/base_classes/NXcg_hexahedron.nxdl.xml
    66 Extracted: definitions-main/base_classes/NXcg_parallelogram.nxdl.xml
    67 Extracted: definitions-main/base_classes/NXcg_point.nxdl.xml
    68 Extracted: definitions-main/base_classes/NXcg_polygon.nxdl.xml
    69 Extracted: definitions-main/base_classes/NXcg_polyhedron.nxdl.xml
    70 Extracted: definitions-main/base_classes/NXcg_polyline.nxdl.xml
    71 Extracted: definitions-main/base_classes/NXcg_primitive.nxdl.xml
    72 Extracted: definitions-main/base_classes/NXcg_roi.nxdl.xml
    73 Extracted: definitions-main/base_classes/NXcg_tetrahedron.nxdl.xml
    74 Extracted: definitions-main/base_classes/NXcg_triangle.nxdl.xml
    75 Extracted: definitions-main/base_classes/NXcg_unit_normal.nxdl.xml
    76 Extracted: definitions-main/base_classes/NXchemical_composition.nxdl.xml
    77 Extracted: definitions-main/base_classes/NXcircuit.nxdl.xml
    78 Extracted: definitions-main/base_classes/NXcite.nxdl.xml
    79 Extracted: definitions-main/base_classes/NXcollection.nxdl.xml
    80 Extracted: definitions-main/base_classes/NXcollectioncolumn.nxdl.xml
    81 Extracted: definitions-main/base_classes/NXcollimator.nxdl.xml
    82 Extracted: definitions-main/base_classes/NXcomponent.nxdl.xml
    83 Extracted: definitions-main/base_classes/NXcoordinate_system.nxdl.xml
    84 Extracted: definitions-main/base_classes/NXcrystal.nxdl.xml
    85 Extracted: definitions-main/base_classes/NXcs_computer.nxdl.xml
    86 Extracted: definitions-main/base_classes/NXcs_filter_boolean_mask.nxdl.xml
    87 Extracted: definitions-main/base_classes/NXcs_memory.nxdl.xml
    88 Extracted: definitions-main/base_classes/NXcs_prng.nxdl.xml
    89 Extracted: definitions-main/base_classes/NXcs_processor.nxdl.xml
    90 Extracted: definitions-main/base_classes/NXcs_profiling.nxdl.xml
    91 Extracted: definitions-main/base_classes/NXcs_profiling_event.nxdl.xml
    92 Extracted: definitions-main/base_classes/NXcs_storage.nxdl.xml
    93 Extracted: definitions-main/base_classes/NXcylindrical_geometry.nxdl.xml
    94 Extracted: definitions-main/base_classes/NXdata.nxdl.xml
    95 Extracted: definitions-main/base_classes/NXdeflector.nxdl.xml
    96 Extracted: definitions-main/base_classes/NXdetector.nxdl.xml
    97 Extracted: definitions-main/base_classes/NXdetector_channel.nxdl.xml
    98 Extracted: definitions-main/base_classes/NXdetector_group.nxdl.xml
    99 Extracted: definitions-main/base_classes/NXdetector_module.nxdl.xml
    100 Extracted: definitions-main/base_classes/NXdisk_chopper.nxdl.xml
    101 Extracted: definitions-main/base_classes/NXdistortion.nxdl.xml
    102 Extracted: definitions-main/base_classes/NXelectron_detector.nxdl.xml
    103 Extracted: definitions-main/base_classes/NXelectronanalyzer.nxdl.xml
    104 Extracted: definitions-main/base_classes/NXenergydispersion.nxdl.xml
    105 Extracted: definitions-main/base_classes/NXentry.nxdl.xml
    106 Extracted: definitions-main/base_classes/NXenvironment.nxdl.xml
    107 Extracted: definitions-main/base_classes/NXevent_data.nxdl.xml
    108 Extracted: definitions-main/base_classes/NXevent_data_apm.nxdl.xml
    109 Extracted: definitions-main/base_classes/NXfabrication.nxdl.xml
    110 Extracted: definitions-main/base_classes/NXfermi_chopper.nxdl.xml
    111 Extracted: definitions-main/base_classes/NXfilter.nxdl.xml
    112 Extracted: definitions-main/base_classes/NXfit.nxdl.xml
    113 Extracted: definitions-main/base_classes/NXfit_function.nxdl.xml
    114 Extracted: definitions-main/base_classes/NXflipper.nxdl.xml
    115 Extracted: definitions-main/base_classes/NXfresnel_zone_plate.nxdl.xml
    116 Extracted: definitions-main/base_classes/NXgeometry.nxdl.xml
    117 Extracted: definitions-main/base_classes/NXgrating.nxdl.xml
    118 Extracted: definitions-main/base_classes/NXguide.nxdl.xml
    119 Extracted: definitions-main/base_classes/NXhistory.nxdl.xml
    120 Extracted: definitions-main/base_classes/NXimage.nxdl.xml
    121 Extracted: definitions-main/base_classes/NXinsertion_device.nxdl.xml
    122 Extracted: definitions-main/base_classes/NXinstrument.nxdl.xml
    123 Extracted: definitions-main/base_classes/NXinstrument_apm.nxdl.xml
    124 Extracted: definitions-main/base_classes/NXlens_em.nxdl.xml
    125 Extracted: definitions-main/base_classes/NXlog.nxdl.xml
    126 Extracted: definitions-main/base_classes/NXmanipulator.nxdl.xml
    127 Extracted: definitions-main/base_classes/NXmirror.nxdl.xml
    128 Extracted: definitions-main/base_classes/NXmoderator.nxdl.xml
    129 Extracted: definitions-main/base_classes/NXmonitor.nxdl.xml
    130 Extracted: definitions-main/base_classes/NXmonochromator.nxdl.xml
    131 Extracted: definitions-main/base_classes/NXnote.nxdl.xml
    132 Extracted: definitions-main/base_classes/NXobject.nxdl.xml
    133 Extracted: definitions-main/base_classes/NXoff_geometry.nxdl.xml
    134 Extracted: definitions-main/base_classes/NXoptical_lens.nxdl.xml
    135 Extracted: definitions-main/base_classes/NXoptical_window.nxdl.xml
    136 Extracted: definitions-main/base_classes/NXorientation.nxdl.xml
    137 Extracted: definitions-main/base_classes/NXparameters.nxdl.xml
    138 Extracted: definitions-main/base_classes/NXpdb.nxdl.xml
    139 Extracted: definitions-main/base_classes/NXpeak.nxdl.xml
    140 Extracted: definitions-main/base_classes/NXpid_controller.nxdl.xml
    141 Extracted: definitions-main/base_classes/NXpinhole.nxdl.xml
    142 Extracted: definitions-main/base_classes/NXpolarizer.nxdl.xml
    143 Extracted: definitions-main/base_classes/NXpositioner.nxdl.xml
    144 Extracted: definitions-main/base_classes/NXprocess.nxdl.xml
    145 Extracted: definitions-main/base_classes/NXprogram.nxdl.xml
    146 Extracted: definitions-main/base_classes/NXpump.nxdl.xml
    147 Extracted: definitions-main/base_classes/NXreflections.nxdl.xml
    148 Extracted: definitions-main/base_classes/NXregistration.nxdl.xml
    149 Extracted: definitions-main/base_classes/NXresolution.nxdl.xml
    150 Extracted: definitions-main/base_classes/NXroi_process.nxdl.xml
    151 Extracted: definitions-main/base_classes/NXroot.nxdl.xml
    152 Extracted: definitions-main/base_classes/NXsample.nxdl.xml
    153 Extracted: definitions-main/base_classes/NXsample_component.nxdl.xml
    154 Extracted: definitions-main/base_classes/NXsensor.nxdl.xml
    155 Extracted: definitions-main/base_classes/NXshape.nxdl.xml
    156 Extracted: definitions-main/base_classes/NXslit.nxdl.xml
    157 Extracted: definitions-main/base_classes/NXsource.nxdl.xml
    158 Extracted: definitions-main/base_classes/NXspectrum.nxdl.xml
    159 Extracted: definitions-main/base_classes/NXspindispersion.nxdl.xml
    160 Extracted: definitions-main/base_classes/NXsubentry.nxdl.xml
    161 Extracted: definitions-main/base_classes/NXtransformations.nxdl.xml
    162 Extracted: definitions-main/base_classes/NXtranslation.nxdl.xml
    163 Extracted: definitions-main/base_classes/NXunit_cell.nxdl.xml
    164 Extracted: definitions-main/base_classes/NXuser.nxdl.xml
    165 Extracted: definitions-main/base_classes/NXvelocity_selector.nxdl.xml
    166 Extracted: definitions-main/base_classes/NXwaveplate.nxdl.xml
    167 Extracted: definitions-main/base_classes/NXxraylens.nxdl.xml
    168 Extracted: definitions-main/base_classes/nxdlformat.xsl
    169 Extracted: definitions-main/contributed_definitions/NXaberration.nxdl.xml
    170 Extracted: definitions-main/contributed_definitions/NXaberration_model.nxdl.xml
    171 Extracted: definitions-main/contributed_definitions/NXaberration_model_ceos.nxdl.xml
    172 Extracted: definitions-main/contributed_definitions/NXaberration_model_nion.nxdl.xml
    173 Extracted: definitions-main/contributed_definitions/NXadc.nxdl.xml
    174 Extracted: definitions-main/contributed_definitions/NXaperture_em.nxdl.xml
    175 Extracted: definitions-main/contributed_definitions/NXapm_composition_space_results.nxdl.xml
    176 Extracted: definitions-main/contributed_definitions/NXapm_input_ranging.nxdl.xml
    177 Extracted: definitions-main/contributed_definitions/NXapm_input_reconstruction.nxdl.xml
    178 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_config_clusterer.nxdl.xml
    179 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_config_distancer.nxdl.xml
    180 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_config_intersector.nxdl.xml
    181 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_config_nanochem.nxdl.xml
    182 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_config_ranger.nxdl.xml
    183 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_config_selector.nxdl.xml
    184 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_config_spatstat.nxdl.xml
    185 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_config_surfacer.nxdl.xml
    186 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_config_tessellator.nxdl.xml
    187 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_config_transcoder.nxdl.xml
    188 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_results_clusterer.nxdl.xml
    189 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_results_distancer.nxdl.xml
    190 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_results_intersector.nxdl.xml
    191 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_results_nanochem.nxdl.xml
    192 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_results_ranger.nxdl.xml
    193 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_results_selector.nxdl.xml
    194 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_results_spatstat.nxdl.xml
    195 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_results_surfacer.nxdl.xml
    196 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_results_tessellator.nxdl.xml
    197 Extracted: definitions-main/contributed_definitions/NXapm_paraprobe_results_transcoder.nxdl.xml
    198 Extracted: definitions-main/contributed_definitions/NXbeam_splitter.nxdl.xml
    199 Extracted: definitions-main/contributed_definitions/NXcircuit_board.nxdl.xml
    200 Extracted: definitions-main/contributed_definitions/NXclustering.nxdl.xml
    201 Extracted: definitions-main/contributed_definitions/NXcontainer.nxdl.xml
    202 Extracted: definitions-main/contributed_definitions/NXcoordinate_system_set.nxdl.xml
    203 Extracted: definitions-main/contributed_definitions/NXcorrector_cs.nxdl.xml
    204 Extracted: definitions-main/contributed_definitions/NXcs_cpu.nxdl.xml
    205 Extracted: definitions-main/contributed_definitions/NXcs_gpu.nxdl.xml
    206 Extracted: definitions-main/contributed_definitions/NXcs_io_obj.nxdl.xml
    207 Extracted: definitions-main/contributed_definitions/NXcs_io_sys.nxdl.xml
    208 Extracted: definitions-main/contributed_definitions/NXcs_mm_sys.nxdl.xml
    209 Extracted: definitions-main/contributed_definitions/NXcsg.nxdl.xml
    210 Extracted: definitions-main/contributed_definitions/NXcxi_ptycho.nxdl.xml
    211 Extracted: definitions-main/contributed_definitions/NXdac.nxdl.xml
    212 Extracted: definitions-main/contributed_definitions/NXdelocalization.nxdl.xml
    213 Extracted: definitions-main/contributed_definitions/NXdispersion.nxdl.xml
    214 Extracted: definitions-main/contributed_definitions/NXdispersion_function.nxdl.xml
    215 Extracted: definitions-main/contributed_definitions/NXdispersion_repeated_parameter.nxdl.xml
    216 Extracted: definitions-main/contributed_definitions/NXdispersion_single_parameter.nxdl.xml
    217 Extracted: definitions-main/contributed_definitions/NXdispersion_table.nxdl.xml
    218 Extracted: definitions-main/contributed_definitions/NXdispersive_material.nxdl.xml
    219 Extracted: definitions-main/contributed_definitions/NXebeam_column.nxdl.xml
    220 Extracted: definitions-main/contributed_definitions/NXelectrostatic_kicker.nxdl.xml
    221 Extracted: definitions-main/contributed_definitions/NXem.nxdl.xml
    222 Extracted: definitions-main/contributed_definitions/NXem_ebsd.nxdl.xml
    223 Extracted: definitions-main/contributed_definitions/NXem_ebsd_conventions.nxdl.xml
    224 Extracted: definitions-main/contributed_definitions/NXem_ebsd_crystal_structure_model.nxdl.xml
    225 Extracted: definitions-main/contributed_definitions/NXevent_data_em.nxdl.xml
    226 Extracted: definitions-main/contributed_definitions/NXevent_data_em_set.nxdl.xml
    227 Extracted: definitions-main/contributed_definitions/NXfiber.nxdl.xml
    228 Extracted: definitions-main/contributed_definitions/NXgraph_edge_set.nxdl.xml
    229 Extracted: definitions-main/contributed_definitions/NXgraph_node_set.nxdl.xml
    230 Extracted: definitions-main/contributed_definitions/NXgraph_root.nxdl.xml
    231 Extracted: definitions-main/contributed_definitions/NXibeam_column.nxdl.xml
    232 Extracted: definitions-main/contributed_definitions/NXimage_set_em_adf.nxdl.xml
    233 Extracted: definitions-main/contributed_definitions/NXimage_set_em_kikuchi.nxdl.xml
    234 Extracted: definitions-main/contributed_definitions/NXinteraction_vol_em.nxdl.xml
    235 Extracted: definitions-main/contributed_definitions/NXion.nxdl.xml
    236 Extracted: definitions-main/contributed_definitions/NXisocontour.nxdl.xml
    237 Extracted: definitions-main/contributed_definitions/NXiv_temp.nxdl.xml
    238 Extracted: definitions-main/contributed_definitions/NXlab_electro_chemo_mechanical_preparation.nxdl.xml
    239 Extracted: definitions-main/contributed_definitions/NXlab_sample_mounting.nxdl.xml
    240 Extracted: definitions-main/contributed_definitions/NXmagnetic_kicker.nxdl.xml
    241 Extracted: definitions-main/contributed_definitions/NXmatch_filter.nxdl.xml
    242 Extracted: definitions-main/contributed_definitions/NXms.nxdl.xml
    243 Extracted: definitions-main/contributed_definitions/NXms_feature_set.nxdl.xml
    244 Extracted: definitions-main/contributed_definitions/NXms_score_config.nxdl.xml
    245 Extracted: definitions-main/contributed_definitions/NXms_score_results.nxdl.xml
    246 Extracted: definitions-main/contributed_definitions/NXms_snapshot.nxdl.xml
    247 Extracted: definitions-main/contributed_definitions/NXms_snapshot_set.nxdl.xml
    248 Extracted: definitions-main/contributed_definitions/NXoptical_system_em.nxdl.xml
    249 Extracted: definitions-main/contributed_definitions/NXorientation_set.nxdl.xml
    250 Extracted: definitions-main/contributed_definitions/NXpolarizer_opt.nxdl.xml
    251 Extracted: definitions-main/contributed_definitions/NXquadric.nxdl.xml
    252 Extracted: definitions-main/contributed_definitions/NXquadrupole_magnet.nxdl.xml
    253 Extracted: definitions-main/contributed_definitions/NXregion.nxdl.xml
    254 Extracted: definitions-main/contributed_definitions/NXscanbox_em.nxdl.xml
    255 Extracted: definitions-main/contributed_definitions/NXsensor_scan.nxdl.xml
    256 Extracted: definitions-main/contributed_definitions/NXseparator.nxdl.xml
    257 Extracted: definitions-main/contributed_definitions/NXsimilarity_grouping.nxdl.xml
    258 Extracted: definitions-main/contributed_definitions/NXslip_system_set.nxdl.xml
    259 Extracted: definitions-main/contributed_definitions/NXsnsevent.nxdl.xml
    260 Extracted: definitions-main/contributed_definitions/NXsnshisto.nxdl.xml
    261 Extracted: definitions-main/contributed_definitions/NXsolenoid_magnet.nxdl.xml
    262 Extracted: definitions-main/contributed_definitions/NXsolid_geometry.nxdl.xml
    263 Extracted: definitions-main/contributed_definitions/NXspatial_filter.nxdl.xml
    264 Extracted: definitions-main/contributed_definitions/NXspectrum_set.nxdl.xml
    265 Extracted: definitions-main/contributed_definitions/NXspectrum_set_em_eels.nxdl.xml
    266 Extracted: definitions-main/contributed_definitions/NXspectrum_set_em_xray.nxdl.xml
    267 Extracted: definitions-main/contributed_definitions/NXspin_rotator.nxdl.xml
    268 Extracted: definitions-main/contributed_definitions/NXsubsampling_filter.nxdl.xml
    269 Extracted: definitions-main/contributed_definitions/NXsubstance.nxdl.xml
    270 Extracted: definitions-main/contributed_definitions/NXtransmission.nxdl.xml
    271 Extracted: definitions-main/contributed_definitions/NXxpcs.nxdl.xml
    272 Extracted: definitions-main/contributed_definitions/nxdlformat.xsl
    273 Extracted: definitions-main/nxdl.xsd
    274 Extracted: definitions-main/nxdlTypes.xsd
    Created: /home/user/.config/punx/definitions-main/__github_info__.json
    Installed in directory: /home/user/.config/punx/main
    ============= ====== =================== ======= =============================================================================================
    NXDL file set cache  date & time         commit  path                                                 
    ============= ====== =================== ======= =============================================================================================
    a4fd52d       source 2016-11-19 01:07:45 a4fd52d /home/user/fairmat/nomad-distro-dev/.venv/lib/python3.12/site-packages/punx/cache/a4fd52d
    v3.3          source 2017-07-12 10:41:12 9285af9 /home/user/fairmat/nomad-distro-dev/.venv/lib/python3.12/site-packages/punx/cache/v3.3
    v2018.5       source 2018-05-15 16:34:19 a3045fd /home/user/fairmat/nomad-distro-dev/.venv/lib/python3.12/site-packages/punx/cache/v2018.5
    main          user   2025-08-14 04:24:42 7ac3f9c /home/user/.config/punx/main                     
    ============= ====== =================== ======= =============================================================================================
    ```

### Usage

After installation, you can invoke the help call from the command line:

=== "Source"
    ```console
    punx --help
    ```

=== "Result"
    ```console
    usage: punx [-h] [-v] {configuration,demonstrate,install,tree,validate} ...

    Python Utilities for NeXus HDF5 files version: 0.3.5 URL: https://prjemian.github.io/punx

    options:
      -h, --help    show this help message and exit
      -v, --version show program's version number and exit

    subcommand:
      valid subcommands

    {configuration,demonstrate,install,tree,validate}
      configuration  show configuration details of punx
      demonstrate    demonstrate HDF5 file validation
      install        install NeXus definitions into the local cache
      tree           show tree structure of HDF5 or NXDL file
      validate       validate a NeXus file

    Note: It is only necessary to use the first two (or more) characters of any subcommand, enough that the abbreviation is unique. Such as: demonstrate can be abbreviated to demo or even de.
    ```

!!! info "NeXus definitions in `punx`"
    The program selects the NeXus definitions (set of nxdl.xml files) by itself. As of July 2025, only the official definitions from the NIAC repository are available.

    You may update the repository for the latest version via:

    ```console
    punx install
    ```

### Validation in `punx`

- [`punx` validation docs](<https://punx.readthedocs.io/en/latest/validate.html#validate>)

You can start the `punx` validation by running

=== "Source"
    ```console
    punx validate src/pynxtools/data/201805_WSe2_arpes.nxs
    ```

=== "Result"

    ```console
    !!! WARNING: this program is not ready for distribution.

    data file: src/pynxtools/data/201805_WSe2_arpes.nxs
    NeXus definitions: main, dated 2025-08-14 04:24:42, sha=7ac3f9c2376bbe8c9c9c942652f0c9c3bfb065fe

    findings
    ======================================================= ======== ==================================== ===========================================================================================
    address                                                 status   test                                 comments                                                                                   
    ======================================================= ======== ==================================== ===========================================================================================
    /                                                       TODO     NeXus base class                     NXroot: more validations needed                                                            
    /                                                       OK       known NXDL                           NXroot: recognized NXDL specification                                                      
    /                                                       OK       NeXus base class                     NXroot: known NeXus base class                                                             
    /                                                       OK       NXDL group in data file              found:  in //entry                                                                         
    /                                                       OK       NeXus default plot                   found by v3: /entry/data/data                                                              
    /@HDF5_Version                                          TODO     attribute value                      implement                                                                                  
    /@HDF5_Version                                          TODO     value of @HDF5_Version               TODO: need to validate: @HDF5_Version = 1.10.5                                             
    /@HDF5_Version                                          OK       validItemName                        relaxed pattern: [a-zA-Z0-9_]([a-zA-Z0-9_.]*[a-zA-Z0-9_])?                                 
    /@HDF5_Version                                          OK       known attribute                      known: NXroot@HDF5_Version                                                                 
    /@file_name                                             TODO     attribute value                      implement                                                                                  
    /@file_name                                             TODO     value of @file_name                  TODO: need to validate: @file_name = /home/tommaso/Desktop/NeXus/Test/201805_WSe2_arpes.nxs
    /@file_name                                             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /@file_name                                             OK       known attribute                      known: NXroot@file_name                                                                    
    /@file_time                                             TODO     attribute value                      implement                                                                                  
    /@file_time                                             TODO     value of @file_time                  TODO: need to validate: @file_time = 2020-06-04T19:19:48.464472                            
    /@file_time                                             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /@file_time                                             OK       known attribute                      known: NXroot@file_time                                                                    
    /@h5py_version                                          TODO     attribute value                      implement                                                                                  
    /@h5py_version                                          TODO     value of @h5py_version               TODO: need to validate: @h5py_version = 2.10.0                                             
    /@h5py_version                                          OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /@h5py_version                                          OK       known attribute                      known: NXroot@h5py_version                                                                 
    /@nexusformat_version                                   TODO     attribute value                      implement                                                                                  
    /@nexusformat_version                                   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /@nexusformat_version                                   OK       known attribute                      unknown: NXroot@nexusformat_version                                                        
    /entry                                                  TODO     NeXus base class                     NXentry: more validations needed                                                           
    /entry                                                  TODO     NeXus application definition         NXarpes: more validations needed                                                           
    /entry                                                  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry                                                  OK       group in base class                  defined: NXroot/entry                                                                      
    /entry                                                  OK       known NXDL                           NXentry: recognized NXDL specification                                                     
    /entry                                                  OK       NeXus base class                     NXentry: known NeXus base class                                                            
    /entry                                                  OK       NXDL field in data file              found: /entry/collection_time                                                              
    /entry                                                  OK       NXDL field in data file              found: /entry/definition                                                                   
    /entry                                                  OK       NXDL field in data file              found: /entry/duration                                                                     
    /entry                                                  OK       NXDL field in data file              found: /entry/end_time                                                                     
    /entry                                                  OK       NXDL field in data file              found: /entry/entry_identifier                                                             
    /entry                                                  OK       NXDL field in data file              found: /entry/experiment_identifier                                                        
    /entry                                                  OK       NXDL field in data file              found: /entry/run_cycle                                                                    
    /entry                                                  OK       NXDL field in data file              found: /entry/start_time                                                                   
    /entry                                                  OK       NXDL field in data file              found: /entry/title                                                                        
    /entry                                                  OK       NXDL group in data file              found:  in /entry/data                                                                     
    /entry                                                  OK       NXDL group in data file              found:  in /entry/instrument                                                               
    /entry                                                  OK       NXDL group in data file              found:  in /entry/sample                                                                   
    /entry                                                  OK       known NXDL                           NXarpes: recognized NXDL specification                                                     
    /entry                                                  OK       NeXus application definition         NXarpes: known NeXus application definition                                                
    /entry                                                  OPTIONAL NXDL field in data file              not found: /entry/collection_description                                                   
    /entry                                                  OPTIONAL NXDL field in data file              not found: /entry/collection_identifier                                                    
    /entry                                                  OPTIONAL NXDL field in data file              not found: /entry/definition_local                                                         
    /entry                                                  OPTIONAL NXDL field in data file              not found: /entry/entry_identifier_uuid                                                    
    /entry                                                  OPTIONAL NXDL field in data file              not found: /entry/experiment_description                                                   
    /entry                                                  OPTIONAL NXDL field in data file              not found: /entry/features                                                                 
    /entry                                                  OPTIONAL NXDL field in data file              not found: /entry/pre_sample_flightpath                                                    
    /entry                                                  OPTIONAL NXDL field in data file              not found: /entry/program_name                                                             
    /entry                                                  OPTIONAL NXDL field in data file              not found: /entry/revision                                                                 
    /entry                                                  OPTIONAL NXDL group in data file              not found:  in /entry/collection                                                           
    /entry                                                  OPTIONAL NXDL group in data file              not found:  in /entry/experiment_documentation                                             
    /entry                                                  OPTIONAL NXDL group in data file              not found:  in /entry/monitor                                                              
    /entry                                                  OPTIONAL NXDL group in data file              not found:  in /entry/notes                                                                
    /entry                                                  OPTIONAL NXDL group in data file              not found:  in /entry/parameters                                                           
    /entry                                                  OPTIONAL NXDL group in data file              not found:  in /entry/process                                                              
    /entry                                                  OPTIONAL NXDL group in data file              not found:  in /entry/subentry                                                             
    /entry                                                  OPTIONAL NXDL group in data file              not found:  in /entry/thumbnail                                                            
    /entry                                                  OPTIONAL NXDL group in data file              not found:  in /entry/user                                                                 
    /entry@NX_class                                         OK       validItemName                        pattern: NX.+                                                                              
    /entry@NX_class                                         OK       attribute value                      recognized NXDL base class: NXentry                                                        
    /entry@NX_class                                         OK       known attribute                      known: NXentry@NX_class                                                                    
    /entry/collection_time                                  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/collection_time                                  OK       field in base class                  defined: NXentry/collection_time                                                           
    /entry/collection_time@units                            TODO     attribute value                      implement                                                                                  
    /entry/collection_time@units                            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/data                                             TODO     NeXus base class                     NXdata: more validations needed                                                            
    /entry/data                                             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/data                                             OK       group in base class                  defined: NXentry/data                                                                      
    /entry/data                                             OK       known NXDL                           NXdata: recognized NXDL specification                                                      
    /entry/data                                             OK       NeXus base class                     NXdata: known NeXus base class                                                             
    /entry/data                                             OPTIONAL NXDL field in data file              not found: /entry/data/AXISNAME                                                            
    /entry/data                                             OPTIONAL NXDL field in data file              not found: /entry/data/DATA                                                                
    /entry/data                                             OPTIONAL NXDL field in data file              not found: /entry/data/FIELDNAME_errors                                                    
    /entry/data                                             OPTIONAL NXDL field in data file              not found: /entry/data/FIELDNAME_offset                                                    
    /entry/data                                             OPTIONAL NXDL field in data file              not found: /entry/data/FIELDNAME_scaling_factor                                            
    /entry/data                                             OPTIONAL NXDL field in data file              not found: /entry/data/errors                                                              
    /entry/data                                             OPTIONAL NXDL field in data file              not found: /entry/data/offset                                                              
    /entry/data                                             OPTIONAL NXDL field in data file              not found: /entry/data/scaling_factor                                                      
    /entry/data                                             OPTIONAL NXDL field in data file              not found: /entry/data/title                                                               
    /entry/data                                             OPTIONAL NXDL field in data file              not found: /entry/data/x                                                                   
    /entry/data                                             OPTIONAL NXDL field in data file              not found: /entry/data/y                                                                   
    /entry/data                                             OPTIONAL NXDL field in data file              not found: /entry/data/z                                                                   
    /entry/data@NX_class                                    OK       validItemName                        pattern: NX.+                                                                              
    /entry/data@NX_class                                    OK       attribute value                      recognized NXDL base class: NXdata                                                         
    /entry/data@NX_class                                    OK       known attribute                      known: NXdata@NX_class                                                                     
    /entry/data@axes                                        TODO     attribute value                      implement                                                                                  
    /entry/data@axes                                        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/data@axes                                        OK       valid name @axes['angles']           strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/data@axes                                        OK       axes['angles'] exists                found field for named axis                                                                 
    /entry/data@axes                                        OK       valid name @axes['energies']         strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/data@axes                                        OK       axes['energies'] exists              found field for named axis                                                                 
    /entry/data@axes                                        OK       valid name @axes['delays']           strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/data@axes                                        OK       axes['delays'] exists                found field for named axis                                                                 
    /entry/data@axes                                        OK       known attribute                      known: NXdata@axes                                                                         
    /entry/data@signal                                      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/data@signal                                      OK       valid name @signal=data              strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/data@signal                                      OK       attribute value                      found: @signal=data                                                                        
    /entry/data@signal                                      OK       known attribute                      known: NXdata@signal                                                                       
    /entry/data@signal                                      OK       value of @signal                     found: /entry/data/data                                                                    
    /entry/data@signal                                      OK       NeXus default plot v3, NXdata@signal correct default plot setup in /NXentry/NXdata                                              
    /entry/data/angles                                      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/data/angles                                      OK       field in base class                  not defined: NXdata/angles                                                                 
    /entry/data/angles@target                               OK       attribute value                      found: @target=/entry/instrument/analyser/angles                                           
    /entry/data/angles@units                                TODO     attribute value                      implement                                                                                  
    /entry/data/data                                        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/data/data                                        OK       field in base class                  not defined: NXdata/data                                                                   
    /entry/data/data@target                                 OK       attribute value                      found: @target=/entry/instrument/analyser/data                                             
    /entry/data/data@units                                  TODO     attribute value                      implement                                                                                  
    /entry/data/delays                                      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/data/delays                                      OK       field in base class                  not defined: NXdata/delays                                                                 
    /entry/data/delays@target                               OK       attribute value                      found: @target=/entry/instrument/analyser/delays                                           
    /entry/data/delays@units                                TODO     attribute value                      implement                                                                                  
    /entry/data/energies                                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/data/energies                                    OK       field in base class                  not defined: NXdata/energies                                                               
    /entry/data/energies@target                             OK       attribute value                      found: @target=/entry/instrument/analyser/energies                                         
    /entry/data/energies@units                              TODO     attribute value                      implement                                                                                  
    /entry/definition                                       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/definition                                       OK       field in base class                  defined: NXentry/definition                                                                
    /entry/definition                                       OK       NXDL field                           NXarpes:definition found                                                                   
    /entry/definition                                       OK       NXDL field enumerations              NXarpes:definition (required) has expected value: NXarpes                                  
    /entry/duration                                         OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/duration                                         OK       field in base class                  defined: NXentry/duration                                                                  
    /entry/duration@units                                   TODO     attribute value                      implement                                                                                  
    /entry/duration@units                                   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/end_time                                         OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/end_time                                         OK       field in base class                  defined: NXentry/end_time                                                                  
    /entry/entry_identifier                                 OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/entry_identifier                                 OK       field in base class                  defined: NXentry/entry_identifier                                                          
    /entry/experiment_identifier                            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/experiment_identifier                            OK       field in base class                  defined: NXentry/experiment_identifier                                                     
    /entry/instrument                                       TODO     NeXus base class                     NXinstrument: more validations needed                                                      
    /entry/instrument                                       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument                                       OK       group in base class                  defined: NXentry/instrument                                                                
    /entry/instrument                                       OK       known NXDL                           NXinstrument: recognized NXDL specification                                                
    /entry/instrument                                       OK       NeXus base class                     NXinstrument: known NeXus base class                                                       
    /entry/instrument                                       OK       NXDL field in data file              found: /entry/instrument/name                                                              
    /entry/instrument                                       OK       NXDL group in data file              found:  in /entry/instrument/monochromator                                                 
    /entry/instrument                                       OK       NXDL group in data file              found:  in /entry/instrument/source                                                        
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/DIFFRACTOMETER                                            
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/actuator                                                  
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/aperture                                                  
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/attenuator                                                
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/beam                                                      
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/beam_stop                                                 
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/bending_magnet                                            
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/capillary                                                 
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/collection                                                
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/collimator                                                
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/crystal                                                   
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/detector                                                  
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/detector_group                                            
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/disk_chopper                                              
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/event_data                                                
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/fabrication                                               
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/fermi_chopper                                             
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/filter                                                    
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/flipper                                                   
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/guide                                                     
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/history                                                   
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/insertion_device                                          
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/mirror                                                    
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/moderator                                                 
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/polarizer                                                 
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/positioner                                                
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/sensor                                                    
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/velocity_selector                                         
    /entry/instrument                                       OPTIONAL NXDL group in data file              not found:  in /entry/instrument/xraylens                                                  
    /entry/instrument@NX_class                              OK       validItemName                        pattern: NX.+                                                                              
    /entry/instrument@NX_class                              OK       attribute value                      recognized NXDL base class: NXinstrument                                                   
    /entry/instrument@NX_class                              OK       known attribute                      known: NXinstrument@NX_class                                                               
    /entry/instrument/analyser                              TODO     NeXus base class                     NXdetector: more validations needed                                                        
    /entry/instrument/analyser                              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser                              OK       group in base class                  not defined: NXinstrument/analyser                                                         
    /entry/instrument/analyser                              OK       known NXDL                           NXdetector: recognized NXDL specification                                                  
    /entry/instrument/analyser                              OK       NeXus base class                     NXdetector: known NeXus base class                                                         
    /entry/instrument/analyser                              OK       NXDL field in data file              found: /entry/instrument/analyser/acquisition_mode                                         
    /entry/instrument/analyser                              OK       NXDL field in data file              found: /entry/instrument/analyser/data                                                     
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/angular_calibration                                  
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/angular_calibration_applied                          
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/azimuthal_angle                                      
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/beam_center_x                                        
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/beam_center_y                                        
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/bit_depth_readout                                    
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/calibration_date                                     
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/count_time                                           
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/countrate_correction_applied                         
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/countrate_correction_lookup_table                    
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/crate                                                
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/data_errors                                          
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/dead_time                                            
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/depends_on                                           
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/description                                          
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/detection_gas_path                                   
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/detector_number                                      
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/detector_readout_time                                
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/diameter                                             
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/distance                                             
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/flatfield                                            
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/flatfield_applied                                    
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/flatfield_errors                                     
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/frame_start_number                                   
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/frame_time                                           
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/gain_setting                                         
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/gas_pressure                                         
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/image_key                                            
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/input                                                
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/layout                                               
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/local_name                                           
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/number_of_cycles                                     
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/pixel_mask                                           
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/pixel_mask_applied                                   
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/polar_angle                                          
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/raw_time_of_flight                                   
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/real_time                                            
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/saturation_value                                     
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/sensor_material                                      
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/sensor_thickness                                     
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/sequence_number                                      
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/serial_number                                        
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/slot                                                 
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/solid_angle                                          
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/start_time                                           
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/stop_time                                            
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/threshold_energy                                     
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/time_of_flight                                       
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/trigger_dead_time                                    
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/trigger_delay_time                                   
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/trigger_delay_time_set                               
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/trigger_internal_delay_time                          
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/type                                                 
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/underload_value                                      
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/virtual_pixel_interpolation_applied                  
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/x_pixel_offset                                       
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/x_pixel_size                                         
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/y_pixel_offset                                       
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/y_pixel_size                                         
    /entry/instrument/analyser                              OPTIONAL NXDL field in data file              not found: /entry/instrument/analyser/z_pixel_offset                                       
    /entry/instrument/analyser                              OPTIONAL NXDL group in data file              not found:  in /entry/instrument/analyser/CHANNELNAME_channel                              
    /entry/instrument/analyser                              OPTIONAL NXDL group in data file              not found:  in /entry/instrument/analyser/calibration_method                               
    /entry/instrument/analyser                              OPTIONAL NXDL group in data file              not found:  in /entry/instrument/analyser/collection                                       
    /entry/instrument/analyser                              OPTIONAL NXDL group in data file              not found:  in /entry/instrument/analyser/data_file                                        
    /entry/instrument/analyser                              OPTIONAL NXDL group in data file              not found:  in /entry/instrument/analyser/detector_module                                  
    /entry/instrument/analyser                              OPTIONAL NXDL group in data file              not found:  in /entry/instrument/analyser/efficiency                                       
    /entry/instrument/analyser                              OPTIONAL NXDL group in data file              not found:  in /entry/instrument/analyser/geometry                                         
    /entry/instrument/analyser@NX_class                     OK       validItemName                        pattern: NX.+                                                                              
    /entry/instrument/analyser@NX_class                     OK       attribute value                      recognized NXDL base class: NXdetector                                                     
    /entry/instrument/analyser@NX_class                     OK       known attribute                      known: NXdetector@NX_class                                                                 
    /entry/instrument/analyser/acquisition_mode             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/acquisition_mode             OK       field in base class                  defined: NXdetector/acquisition_mode                                                       
    /entry/instrument/analyser/amplifier_type               OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/amplifier_type               OK       field in base class                  not defined: NXdetector/amplifier_type                                                     
    /entry/instrument/analyser/angles                       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/angles                       OK       field in base class                  not defined: NXdetector/angles                                                             
    /entry/instrument/analyser/angles@target                OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/angles@target                OK       attribute value                      found: @target=/entry/instrument/analyser/angles                                           
    /entry/instrument/analyser/angles@units                 TODO     attribute value                      implement                                                                                  
    /entry/instrument/analyser/angles@units                 OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/contrast_aperture            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/contrast_aperture            OK       field in base class                  not defined: NXdetector/contrast_aperture                                                  
    /entry/instrument/analyser/data                         OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/data                         OK       field in base class                  defined: NXdetector/data                                                                   
    /entry/instrument/analyser/data@target                  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/data@target                  OK       attribute value                      found: @target=/entry/instrument/analyser/data                                             
    /entry/instrument/analyser/data@units                   TODO     attribute value                      implement                                                                                  
    /entry/instrument/analyser/data@units                   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/delays                       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/delays                       OK       field in base class                  not defined: NXdetector/delays                                                             
    /entry/instrument/analyser/delays@target                OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/delays@target                OK       attribute value                      found: @target=/entry/instrument/analyser/delays                                           
    /entry/instrument/analyser/delays@units                 TODO     attribute value                      implement                                                                                  
    /entry/instrument/analyser/delays@units                 OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/detector_type                OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/detector_type                OK       field in base class                  not defined: NXdetector/detector_type                                                      
    /entry/instrument/analyser/dispersion_scheme            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/dispersion_scheme            OK       field in base class                  not defined: NXdetector/dispersion_scheme                                                  
    /entry/instrument/analyser/energies                     OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/energies                     OK       field in base class                  not defined: NXdetector/energies                                                           
    /entry/instrument/analyser/energies@target              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/energies@target              OK       attribute value                      found: @target=/entry/instrument/analyser/energies                                         
    /entry/instrument/analyser/energies@units               TODO     attribute value                      implement                                                                                  
    /entry/instrument/analyser/energies@units               OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/entrance_slit_setting        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/entrance_slit_setting        OK       field in base class                  not defined: NXdetector/entrance_slit_setting                                              
    /entry/instrument/analyser/entrance_slit_shape          OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/entrance_slit_shape          OK       field in base class                  not defined: NXdetector/entrance_slit_shape                                                
    /entry/instrument/analyser/entrance_slit_size           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/entrance_slit_size           OK       field in base class                  not defined: NXdetector/entrance_slit_size                                                 
    /entry/instrument/analyser/entrance_slit_size@units     TODO     attribute value                      implement                                                                                  
    /entry/instrument/analyser/entrance_slit_size@units     OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/extractor_voltage            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/extractor_voltage            OK       field in base class                  not defined: NXdetector/extractor_voltage                                                  
    /entry/instrument/analyser/extractor_voltage@units      TODO     attribute value                      implement                                                                                  
    /entry/instrument/analyser/extractor_voltage@units      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/field_aperture_x             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/field_aperture_x             OK       field in base class                  not defined: NXdetector/field_aperture_x                                                   
    /entry/instrument/analyser/field_aperture_x@units       TODO     attribute value                      implement                                                                                  
    /entry/instrument/analyser/field_aperture_x@units       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/field_aperture_y             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/field_aperture_y             OK       field in base class                  not defined: NXdetector/field_aperture_y                                                   
    /entry/instrument/analyser/field_aperture_y@units       TODO     attribute value                      implement                                                                                  
    /entry/instrument/analyser/field_aperture_y@units       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/lens_mode                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/lens_mode                    OK       field in base class                  not defined: NXdetector/lens_mode                                                          
    /entry/instrument/analyser/magnification                OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/magnification                OK       field in base class                  not defined: NXdetector/magnification                                                      
    /entry/instrument/analyser/pass_energy                  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/pass_energy                  OK       field in base class                  not defined: NXdetector/pass_energy                                                        
    /entry/instrument/analyser/pass_energy@units            TODO     attribute value                      implement                                                                                  
    /entry/instrument/analyser/pass_energy@units            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/projection                   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/projection                   OK       field in base class                  not defined: NXdetector/projection                                                         
    /entry/instrument/analyser/region_origin                OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/region_origin                OK       field in base class                  not defined: NXdetector/region_origin                                                      
    /entry/instrument/analyser/region_size                  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/region_size                  OK       field in base class                  not defined: NXdetector/region_size                                                        
    /entry/instrument/analyser/sensor_count                 OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/sensor_count                 OK       field in base class                  not defined: NXdetector/sensor_count                                                       
    /entry/instrument/analyser/sensor_size                  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/sensor_size                  OK       field in base class                  not defined: NXdetector/sensor_size                                                        
    /entry/instrument/analyser/time_per_channel             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/time_per_channel             OK       field in base class                  not defined: NXdetector/time_per_channel                                                   
    /entry/instrument/analyser/time_per_channel@units       TODO     attribute value                      implement                                                                                  
    /entry/instrument/analyser/time_per_channel@units       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/working_distance             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/analyser/working_distance             OK       field in base class                  not defined: NXdetector/working_distance                                                   
    /entry/instrument/analyser/working_distance@units       TODO     attribute value                      implement                                                                                  
    /entry/instrument/analyser/working_distance@units       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0                          TODO     NeXus base class                     NXbeam: more validations needed                                                            
    /entry/instrument/beam_probe_0                          OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0                          OK       group in base class                  not defined: NXinstrument/beam_probe_0                                                     
    /entry/instrument/beam_probe_0                          OK       known NXDL                           NXbeam: recognized NXDL specification                                                      
    /entry/instrument/beam_probe_0                          OK       NeXus base class                     NXbeam: known NeXus base class                                                             
    /entry/instrument/beam_probe_0                          OK       NXDL field in data file              found: /entry/instrument/beam_probe_0/distance                                             
    /entry/instrument/beam_probe_0                          OK       NXDL field in data file              found: /entry/instrument/beam_probe_0/pulse_duration                                       
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/average_power                                    
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/chirp_GDD                                        
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/chirp_type                                       
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/depends_on                                       
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/energy_transfer                                  
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/extent                                           
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/final_beam_divergence                            
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/final_energy                                     
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/final_polarization                               
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/final_polarization_stokes                        
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/final_wavelength                                 
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/final_wavelength_spread                          
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/fluence                                          
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/flux                                             
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/frog_delays                                      
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/frog_frequencies                                 
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/frog_trace                                       
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/incident_beam_divergence                         
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/incident_energy                                  
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/incident_energy_spread                           
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/incident_energy_weights                          
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/incident_polarization                            
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/incident_polarization_stokes                     
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/incident_wavelength                              
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/incident_wavelength_spread                       
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/incident_wavelength_weights                      
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/pulse_delay                                      
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_probe_0/pulse_energy                                     
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL group in data file              not found:  in /entry/instrument/beam_probe_0/data                                         
    /entry/instrument/beam_probe_0                          OPTIONAL NXDL group in data file              not found:  in /entry/instrument/beam_probe_0/transformations                              
    /entry/instrument/beam_probe_0@NX_class                 OK       validItemName                        pattern: NX.+                                                                              
    /entry/instrument/beam_probe_0@NX_class                 OK       attribute value                      recognized NXDL base class: NXbeam                                                         
    /entry/instrument/beam_probe_0@NX_class                 OK       known attribute                      known: NXbeam@NX_class                                                                     
    /entry/instrument/beam_probe_0/distance                 OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0/distance                 OK       field in base class                  defined: NXbeam/distance                                                                   
    /entry/instrument/beam_probe_0/distance@units           TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_probe_0/distance@units           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0/photon_energy            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0/photon_energy            OK       field in base class                  not defined: NXbeam/photon_energy                                                          
    /entry/instrument/beam_probe_0/photon_energy@units      TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_probe_0/photon_energy@units      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0/polarization_angle       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0/polarization_angle       OK       field in base class                  not defined: NXbeam/polarization_angle                                                     
    /entry/instrument/beam_probe_0/polarization_angle@units TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_probe_0/polarization_angle@units OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0/polarization_ellipticity OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0/polarization_ellipticity OK       field in base class                  not defined: NXbeam/polarization_ellipticity                                               
    /entry/instrument/beam_probe_0/pulse_duration           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0/pulse_duration           OK       field in base class                  defined: NXbeam/pulse_duration                                                             
    /entry/instrument/beam_probe_0/pulse_duration@units     TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_probe_0/pulse_duration@units     OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0/size_x                   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0/size_x                   OK       field in base class                  not defined: NXbeam/size_x                                                                 
    /entry/instrument/beam_probe_0/size_x@units             TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_probe_0/size_x@units             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0/size_y                   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_probe_0/size_y                   OK       field in base class                  not defined: NXbeam/size_y                                                                 
    /entry/instrument/beam_probe_0/size_y@units             TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_probe_0/size_y@units             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0                           TODO     NeXus base class                     NXbeam: more validations needed                                                            
    /entry/instrument/beam_pump_0                           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0                           OK       group in base class                  not defined: NXinstrument/beam_pump_0                                                      
    /entry/instrument/beam_pump_0                           OK       known NXDL                           NXbeam: recognized NXDL specification                                                      
    /entry/instrument/beam_pump_0                           OK       NeXus base class                     NXbeam: known NeXus base class                                                             
    /entry/instrument/beam_pump_0                           OK       NXDL field in data file              found: /entry/instrument/beam_pump_0/average_power                                         
    /entry/instrument/beam_pump_0                           OK       NXDL field in data file              found: /entry/instrument/beam_pump_0/distance                                              
    /entry/instrument/beam_pump_0                           OK       NXDL field in data file              found: /entry/instrument/beam_pump_0/fluence                                               
    /entry/instrument/beam_pump_0                           OK       NXDL field in data file              found: /entry/instrument/beam_pump_0/pulse_duration                                        
    /entry/instrument/beam_pump_0                           OK       NXDL field in data file              found: /entry/instrument/beam_pump_0/pulse_energy                                          
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/chirp_GDD                                         
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/chirp_type                                        
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/depends_on                                        
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/energy_transfer                                   
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/extent                                            
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/final_beam_divergence                             
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/final_energy                                      
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/final_polarization                                
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/final_polarization_stokes                         
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/final_wavelength                                  
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/final_wavelength_spread                           
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/flux                                              
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/frog_delays                                       
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/frog_frequencies                                  
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/frog_trace                                        
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/incident_beam_divergence                          
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/incident_energy                                   
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/incident_energy_spread                            
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/incident_energy_weights                           
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/incident_polarization                             
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/incident_polarization_stokes                      
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/incident_wavelength                               
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/incident_wavelength_spread                        
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/incident_wavelength_weights                       
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL field in data file              not found: /entry/instrument/beam_pump_0/pulse_delay                                       
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL group in data file              not found:  in /entry/instrument/beam_pump_0/data                                          
    /entry/instrument/beam_pump_0                           OPTIONAL NXDL group in data file              not found:  in /entry/instrument/beam_pump_0/transformations                               
    /entry/instrument/beam_pump_0@NX_class                  OK       validItemName                        pattern: NX.+                                                                              
    /entry/instrument/beam_pump_0@NX_class                  OK       attribute value                      recognized NXDL base class: NXbeam                                                         
    /entry/instrument/beam_pump_0@NX_class                  OK       known attribute                      known: NXbeam@NX_class                                                                     
    /entry/instrument/beam_pump_0/average_power             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/average_power             OK       field in base class                  defined: NXbeam/average_power                                                              
    /entry/instrument/beam_pump_0/average_power@units       TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_pump_0/average_power@units       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/center_wavelength         OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/center_wavelength         OK       field in base class                  not defined: NXbeam/center_wavelength                                                      
    /entry/instrument/beam_pump_0/center_wavelength@units   TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_pump_0/center_wavelength@units   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/distance                  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/distance                  OK       field in base class                  defined: NXbeam/distance                                                                   
    /entry/instrument/beam_pump_0/distance@units            TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_pump_0/distance@units            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/fluence                   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/fluence                   OK       field in base class                  defined: NXbeam/fluence                                                                    
    /entry/instrument/beam_pump_0/fluence@units             TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_pump_0/fluence@units             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/photon_energy             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/photon_energy             OK       field in base class                  not defined: NXbeam/photon_energy                                                          
    /entry/instrument/beam_pump_0/photon_energy@units       TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_pump_0/photon_energy@units       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/polarization_angle        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/polarization_angle        OK       field in base class                  not defined: NXbeam/polarization_angle                                                     
    /entry/instrument/beam_pump_0/polarization_angle@units  TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_pump_0/polarization_angle@units  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/polarization_ellipticity  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/polarization_ellipticity  OK       field in base class                  not defined: NXbeam/polarization_ellipticity                                               
    /entry/instrument/beam_pump_0/pulse_duration            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/pulse_duration            OK       field in base class                  defined: NXbeam/pulse_duration                                                             
    /entry/instrument/beam_pump_0/pulse_duration@units      TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_pump_0/pulse_duration@units      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/pulse_energy              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/pulse_energy              OK       field in base class                  defined: NXbeam/pulse_energy                                                               
    /entry/instrument/beam_pump_0/pulse_energy@units        TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_pump_0/pulse_energy@units        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/size_x                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/size_x                    OK       field in base class                  not defined: NXbeam/size_x                                                                 
    /entry/instrument/beam_pump_0/size_x@units              TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_pump_0/size_x@units              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/size_y                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/beam_pump_0/size_y                    OK       field in base class                  not defined: NXbeam/size_y                                                                 
    /entry/instrument/beam_pump_0/size_y@units              TODO     attribute value                      implement                                                                                  
    /entry/instrument/beam_pump_0/size_y@units              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/energy_resolution                     OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/energy_resolution                     OK       field in base class                  not defined: NXinstrument/energy_resolution                                                
    /entry/instrument/energy_resolution@units               TODO     attribute value                      implement                                                                                  
    /entry/instrument/energy_resolution@units               OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator                           TODO     NeXus base class                     NXpositioner: more validations needed                                                      
    /entry/instrument/manipulator                           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator                           OK       group in base class                  not defined: NXinstrument/manipulator                                                      
    /entry/instrument/manipulator                           OK       known NXDL                           NXpositioner: recognized NXDL specification                                                
    /entry/instrument/manipulator                           OK       NeXus base class                     NXpositioner: known NeXus base class                                                       
    /entry/instrument/manipulator                           OPTIONAL NXDL field in data file              not found: /entry/instrument/manipulator/acceleration_time                                 
    /entry/instrument/manipulator                           OPTIONAL NXDL field in data file              not found: /entry/instrument/manipulator/controller_record                                 
    /entry/instrument/manipulator                           OPTIONAL NXDL field in data file              not found: /entry/instrument/manipulator/depends_on                                        
    /entry/instrument/manipulator                           OPTIONAL NXDL field in data file              not found: /entry/instrument/manipulator/description                                       
    /entry/instrument/manipulator                           OPTIONAL NXDL field in data file              not found: /entry/instrument/manipulator/name                                              
    /entry/instrument/manipulator                           OPTIONAL NXDL field in data file              not found: /entry/instrument/manipulator/raw_value                                         
    /entry/instrument/manipulator                           OPTIONAL NXDL field in data file              not found: /entry/instrument/manipulator/soft_limit_max                                    
    /entry/instrument/manipulator                           OPTIONAL NXDL field in data file              not found: /entry/instrument/manipulator/soft_limit_min                                    
    /entry/instrument/manipulator                           OPTIONAL NXDL field in data file              not found: /entry/instrument/manipulator/target_value                                      
    /entry/instrument/manipulator                           OPTIONAL NXDL field in data file              not found: /entry/instrument/manipulator/tolerance                                         
    /entry/instrument/manipulator                           OPTIONAL NXDL field in data file              not found: /entry/instrument/manipulator/value                                             
    /entry/instrument/manipulator                           OPTIONAL NXDL field in data file              not found: /entry/instrument/manipulator/velocity                                          
    /entry/instrument/manipulator@NX_class                  OK       validItemName                        pattern: NX.+                                                                              
    /entry/instrument/manipulator@NX_class                  OK       attribute value                      recognized NXDL base class: NXpositioner                                                   
    /entry/instrument/manipulator@NX_class                  OK       known attribute                      known: NXpositioner@NX_class                                                               
    /entry/instrument/manipulator/pos_x1                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/pos_x1                    OK       field in base class                  not defined: NXpositioner/pos_x1                                                           
    /entry/instrument/manipulator/pos_x1@units              TODO     attribute value                      implement                                                                                  
    /entry/instrument/manipulator/pos_x1@units              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/pos_x2                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/pos_x2                    OK       field in base class                  not defined: NXpositioner/pos_x2                                                           
    /entry/instrument/manipulator/pos_x2@units              TODO     attribute value                      implement                                                                                  
    /entry/instrument/manipulator/pos_x2@units              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/pos_y                     OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/pos_y                     OK       field in base class                  not defined: NXpositioner/pos_y                                                            
    /entry/instrument/manipulator/pos_y@units               TODO     attribute value                      implement                                                                                  
    /entry/instrument/manipulator/pos_y@units               OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/pos_z1                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/pos_z1                    OK       field in base class                  not defined: NXpositioner/pos_z1                                                           
    /entry/instrument/manipulator/pos_z1@units              TODO     attribute value                      implement                                                                                  
    /entry/instrument/manipulator/pos_z1@units              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/pos_z2                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/pos_z2                    OK       field in base class                  not defined: NXpositioner/pos_z2                                                           
    /entry/instrument/manipulator/pos_z2@units              TODO     attribute value                      implement                                                                                  
    /entry/instrument/manipulator/pos_z2@units              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/pos_z3                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/pos_z3                    OK       field in base class                  not defined: NXpositioner/pos_z3                                                           
    /entry/instrument/manipulator/pos_z3@units              TODO     attribute value                      implement                                                                                  
    /entry/instrument/manipulator/pos_z3@units              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/sample_bias               OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/sample_bias               OK       field in base class                  not defined: NXpositioner/sample_bias                                                      
    /entry/instrument/manipulator/sample_bias@target        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/sample_bias@target        OK       attribute value                      found: @target=/entry/instrument/manipulator/sample_bias                                   
    /entry/instrument/manipulator/sample_bias@units         TODO     attribute value                      implement                                                                                  
    /entry/instrument/manipulator/sample_bias@units         OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/sample_temperature        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/sample_temperature        OK       field in base class                  not defined: NXpositioner/sample_temperature                                               
    /entry/instrument/manipulator/sample_temperature@target OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/sample_temperature@target OK       attribute value                      found: @target=/entry/instrument/manipulator/sample_temperature                            
    /entry/instrument/manipulator/sample_temperature@units  TODO     attribute value                      implement                                                                                  
    /entry/instrument/manipulator/sample_temperature@units  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/type                      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/manipulator/type                      OK       field in base class                  not defined: NXpositioner/type                                                             
    /entry/instrument/monochromator                         TODO     NeXus base class                     NXmonochromator: more validations needed                                                   
    /entry/instrument/monochromator                         OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/monochromator                         OK       group in base class                  defined: NXinstrument/monochromator                                                        
    /entry/instrument/monochromator                         OK       known NXDL                           NXmonochromator: recognized NXDL specification                                             
    /entry/instrument/monochromator                         OK       NeXus base class                     NXmonochromator: known NeXus base class                                                    
    /entry/instrument/monochromator                         OK       NXDL field in data file              found: /entry/instrument/monochromator/energy                                              
    /entry/instrument/monochromator                         OK       NXDL field in data file              found: /entry/instrument/monochromator/energy_error                                        
    /entry/instrument/monochromator                         OPTIONAL NXDL field in data file              not found: /entry/instrument/monochromator/depends_on                                      
    /entry/instrument/monochromator                         OPTIONAL NXDL field in data file              not found: /entry/instrument/monochromator/energy_dispersion                               
    /entry/instrument/monochromator                         OPTIONAL NXDL field in data file              not found: /entry/instrument/monochromator/energy_errors                                   
    /entry/instrument/monochromator                         OPTIONAL NXDL field in data file              not found: /entry/instrument/monochromator/wavelength                                      
    /entry/instrument/monochromator                         OPTIONAL NXDL field in data file              not found: /entry/instrument/monochromator/wavelength_dispersion                           
    /entry/instrument/monochromator                         OPTIONAL NXDL field in data file              not found: /entry/instrument/monochromator/wavelength_error                                
    /entry/instrument/monochromator                         OPTIONAL NXDL field in data file              not found: /entry/instrument/monochromator/wavelength_errors                               
    /entry/instrument/monochromator                         OPTIONAL NXDL group in data file              not found:  in /entry/instrument/monochromator/crystal                                     
    /entry/instrument/monochromator                         OPTIONAL NXDL group in data file              not found:  in /entry/instrument/monochromator/distribution                                
    /entry/instrument/monochromator                         OPTIONAL NXDL group in data file              not found:  in /entry/instrument/monochromator/entrance_slit                               
    /entry/instrument/monochromator                         OPTIONAL NXDL group in data file              not found:  in /entry/instrument/monochromator/exit_slit                                   
    /entry/instrument/monochromator                         OPTIONAL NXDL group in data file              not found:  in /entry/instrument/monochromator/geometry                                    
    /entry/instrument/monochromator                         OPTIONAL NXDL group in data file              not found:  in /entry/instrument/monochromator/grating                                     
    /entry/instrument/monochromator                         OPTIONAL NXDL group in data file              not found:  in /entry/instrument/monochromator/off_geometry                                
    /entry/instrument/monochromator                         OPTIONAL NXDL group in data file              not found:  in /entry/instrument/monochromator/velocity_selector                           
    /entry/instrument/monochromator@NX_class                OK       validItemName                        pattern: NX.+                                                                              
    /entry/instrument/monochromator@NX_class                OK       attribute value                      recognized NXDL base class: NXmonochromator                                                
    /entry/instrument/monochromator@NX_class                OK       known attribute                      known: NXmonochromator@NX_class                                                            
    /entry/instrument/monochromator/energy                  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/monochromator/energy                  OK       field in base class                  defined: NXmonochromator/energy                                                            
    /entry/instrument/monochromator/energy@units            TODO     attribute value                      implement                                                                                  
    /entry/instrument/monochromator/energy@units            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/monochromator/energy_error            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/monochromator/energy_error            OK       field in base class                  defined: NXmonochromator/energy_error                                                      
    /entry/instrument/monochromator/energy_error@units      TODO     attribute value                      implement                                                                                  
    /entry/instrument/monochromator/energy_error@units      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/monochromator/slit                    TODO     NeXus base class                     NXslit: more validations needed                                                            
    /entry/instrument/monochromator/slit                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/monochromator/slit                    OK       group in base class                  not defined: NXmonochromator/slit                                                          
    /entry/instrument/monochromator/slit                    OK       known NXDL                           NXslit: recognized NXDL specification                                                      
    /entry/instrument/monochromator/slit                    OK       NeXus base class                     NXslit: known NeXus base class                                                             
    /entry/instrument/monochromator/slit                    OK       NXDL field in data file              found: /entry/instrument/monochromator/slit/y_gap                                          
    /entry/instrument/monochromator/slit                    OPTIONAL NXDL field in data file              not found: /entry/instrument/monochromator/slit/depends_on                                 
    /entry/instrument/monochromator/slit                    OPTIONAL NXDL field in data file              not found: /entry/instrument/monochromator/slit/x_gap                                      
    /entry/instrument/monochromator/slit@NX_class           OK       validItemName                        pattern: NX.+                                                                              
    /entry/instrument/monochromator/slit@NX_class           OK       attribute value                      recognized NXDL base class: NXslit                                                         
    /entry/instrument/monochromator/slit@NX_class           OK       known attribute                      known: NXslit@NX_class                                                                     
    /entry/instrument/monochromator/slit/y_gap              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/monochromator/slit/y_gap              OK       field in base class                  defined: NXslit/y_gap                                                                      
    /entry/instrument/monochromator/slit/y_gap@units        TODO     attribute value                      implement                                                                                  
    /entry/instrument/monochromator/slit/y_gap@units        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/name                                  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/name                                  OK       field in base class                  defined: NXinstrument/name                                                                 
    /entry/instrument/source                                TODO     NeXus base class                     NXsource: more validations needed                                                          
    /entry/instrument/source                                OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source                                OK       group in base class                  defined: NXinstrument/source                                                               
    /entry/instrument/source                                OK       known NXDL                           NXsource: recognized NXDL specification                                                    
    /entry/instrument/source                                OK       NeXus base class                     NXsource: known NeXus base class                                                           
    /entry/instrument/source                                OK       NXDL field in data file              found: /entry/instrument/source/bunch_distance                                             
    /entry/instrument/source                                OK       NXDL field in data file              found: /entry/instrument/source/bunch_length                                               
    /entry/instrument/source                                OK       NXDL field in data file              found: /entry/instrument/source/current                                                    
    /entry/instrument/source                                OK       NXDL field in data file              found: /entry/instrument/source/energy                                                     
    /entry/instrument/source                                OK       NXDL field in data file              found: /entry/instrument/source/frequency                                                  
    /entry/instrument/source                                OK       NXDL field in data file              found: /entry/instrument/source/mode                                                       
    /entry/instrument/source                                OK       NXDL field in data file              found: /entry/instrument/source/name                                                       
    /entry/instrument/source                                OK       NXDL field in data file              found: /entry/instrument/source/number_of_bunches                                          
    /entry/instrument/source                                OK       NXDL field in data file              found: /entry/instrument/source/probe                                                      
    /entry/instrument/source                                OK       NXDL field in data file              found: /entry/instrument/source/top_up                                                     
    /entry/instrument/source                                OK       NXDL field in data file              found: /entry/instrument/source/type                                                       
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/anode_material                                         
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/depends_on                                             
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/distance                                               
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/emission_current                                       
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/emittance_x                                            
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/emittance_y                                            
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/filament_current                                       
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/flux                                                   
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/gas_pressure                                           
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/last_fill                                              
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/peak_power                                             
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/period                                                 
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/power                                                  
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/previous_source                                        
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/pulse_energy                                           
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/pulse_width                                            
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/sigma_x                                                
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/sigma_y                                                
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/target_material                                        
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/voltage                                                
    /entry/instrument/source                                OPTIONAL NXDL field in data file              not found: /entry/instrument/source/wavelength                                             
    /entry/instrument/source                                OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source/aperture                                           
    /entry/instrument/source                                OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source/bunch_pattern                                      
    /entry/instrument/source                                OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source/deflector                                          
    /entry/instrument/source                                OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source/distribution                                       
    /entry/instrument/source                                OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source/fabrication                                        
    /entry/instrument/source                                OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source/geometry                                           
    /entry/instrument/source                                OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source/lens_em                                            
    /entry/instrument/source                                OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source/notes                                              
    /entry/instrument/source                                OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source/off_geometry                                       
    /entry/instrument/source                                OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source/pulse_shape                                        
    /entry/instrument/source@NX_class                       OK       validItemName                        pattern: NX.+                                                                              
    /entry/instrument/source@NX_class                       OK       attribute value                      recognized NXDL base class: NXsource                                                       
    /entry/instrument/source@NX_class                       OK       known attribute                      known: NXsource@NX_class                                                                   
    /entry/instrument/source/bunch_distance                 OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/bunch_distance                 OK       field in base class                  defined: NXsource/bunch_distance                                                           
    /entry/instrument/source/bunch_distance@units           TODO     attribute value                      implement                                                                                  
    /entry/instrument/source/bunch_distance@units           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/bunch_length                   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/bunch_length                   OK       field in base class                  defined: NXsource/bunch_length                                                             
    /entry/instrument/source/bunch_length@units             TODO     attribute value                      implement                                                                                  
    /entry/instrument/source/bunch_length@units             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/burst_distance                 OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/burst_distance                 OK       field in base class                  not defined: NXsource/burst_distance                                                       
    /entry/instrument/source/burst_distance@units           TODO     attribute value                      implement                                                                                  
    /entry/instrument/source/burst_distance@units           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/burst_length                   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/burst_length                   OK       field in base class                  not defined: NXsource/burst_length                                                         
    /entry/instrument/source/burst_length@units             TODO     attribute value                      implement                                                                                  
    /entry/instrument/source/burst_length@units             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/burst_number_end               OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/burst_number_end               OK       field in base class                  not defined: NXsource/burst_number_end                                                     
    /entry/instrument/source/burst_number_start             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/burst_number_start             OK       field in base class                  not defined: NXsource/burst_number_start                                                   
    /entry/instrument/source/current                        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/current                        OK       field in base class                  defined: NXsource/current                                                                  
    /entry/instrument/source/current@units                  TODO     attribute value                      implement                                                                                  
    /entry/instrument/source/current@units                  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/energy                         OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/energy                         OK       field in base class                  defined: NXsource/energy                                                                   
    /entry/instrument/source/energy@units                   TODO     attribute value                      implement                                                                                  
    /entry/instrument/source/energy@units                   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/frequency                      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/frequency                      OK       field in base class                  defined: NXsource/frequency                                                                
    /entry/instrument/source/frequency@units                TODO     attribute value                      implement                                                                                  
    /entry/instrument/source/frequency@units                OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/mode                           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/mode                           OK       field in base class                  defined: NXsource/mode                                                                     
    /entry/instrument/source/name                           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/name                           OK       field in base class                  defined: NXsource/name                                                                     
    /entry/instrument/source/number_of_bunches              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/number_of_bunches              OK       field in base class                  defined: NXsource/number_of_bunches                                                        
    /entry/instrument/source/number_of_bursts               OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/number_of_bursts               OK       field in base class                  not defined: NXsource/number_of_bursts                                                     
    /entry/instrument/source/probe                          OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/probe                          OK       field in base class                  defined: NXsource/probe                                                                    
    /entry/instrument/source/top_up                         OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/top_up                         OK       field in base class                  defined: NXsource/top_up                                                                   
    /entry/instrument/source/type                           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source/type                           OK       field in base class                  defined: NXsource/type                                                                     
    /entry/instrument/source_pump                           TODO     NeXus base class                     NXsource: more validations needed                                                          
    /entry/instrument/source_pump                           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump                           OK       group in base class                  not defined: NXinstrument/source_pump                                                      
    /entry/instrument/source_pump                           OK       known NXDL                           NXsource: recognized NXDL specification                                                    
    /entry/instrument/source_pump                           OK       NeXus base class                     NXsource: known NeXus base class                                                           
    /entry/instrument/source_pump                           OK       NXDL field in data file              found: /entry/instrument/source_pump/bunch_distance                                        
    /entry/instrument/source_pump                           OK       NXDL field in data file              found: /entry/instrument/source_pump/bunch_length                                          
    /entry/instrument/source_pump                           OK       NXDL field in data file              found: /entry/instrument/source_pump/frequency                                             
    /entry/instrument/source_pump                           OK       NXDL field in data file              found: /entry/instrument/source_pump/mode                                                  
    /entry/instrument/source_pump                           OK       NXDL field in data file              found: /entry/instrument/source_pump/name                                                  
    /entry/instrument/source_pump                           OK       NXDL field in data file              found: /entry/instrument/source_pump/number_of_bunches                                     
    /entry/instrument/source_pump                           OK       NXDL field in data file              found: /entry/instrument/source_pump/probe                                                 
    /entry/instrument/source_pump                           OK       NXDL field in data file              found: /entry/instrument/source_pump/type                                                  
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/anode_material                                    
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/current                                           
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/depends_on                                        
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/distance                                          
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/emission_current                                  
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/emittance_x                                       
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/emittance_y                                       
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/energy                                            
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/filament_current                                  
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/flux                                              
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/gas_pressure                                      
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/last_fill                                         
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/peak_power                                        
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/period                                            
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/power                                             
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/previous_source                                   
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/pulse_energy                                      
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/pulse_width                                       
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/sigma_x                                           
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/sigma_y                                           
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/target_material                                   
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/top_up                                            
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/voltage                                           
    /entry/instrument/source_pump                           OPTIONAL NXDL field in data file              not found: /entry/instrument/source_pump/wavelength                                        
    /entry/instrument/source_pump                           OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source_pump/aperture                                      
    /entry/instrument/source_pump                           OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source_pump/bunch_pattern                                 
    /entry/instrument/source_pump                           OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source_pump/deflector                                     
    /entry/instrument/source_pump                           OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source_pump/distribution                                  
    /entry/instrument/source_pump                           OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source_pump/fabrication                                   
    /entry/instrument/source_pump                           OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source_pump/geometry                                      
    /entry/instrument/source_pump                           OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source_pump/lens_em                                       
    /entry/instrument/source_pump                           OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source_pump/notes                                         
    /entry/instrument/source_pump                           OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source_pump/off_geometry                                  
    /entry/instrument/source_pump                           OPTIONAL NXDL group in data file              not found:  in /entry/instrument/source_pump/pulse_shape                                   
    /entry/instrument/source_pump@NX_class                  OK       validItemName                        pattern: NX.+                                                                              
    /entry/instrument/source_pump@NX_class                  OK       attribute value                      recognized NXDL base class: NXsource                                                       
    /entry/instrument/source_pump@NX_class                  OK       known attribute                      known: NXsource@NX_class                                                                   
    /entry/instrument/source_pump/bunch_distance            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/bunch_distance            OK       field in base class                  defined: NXsource/bunch_distance                                                           
    /entry/instrument/source_pump/bunch_distance@units      TODO     attribute value                      implement                                                                                  
    /entry/instrument/source_pump/bunch_distance@units      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/bunch_length              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/bunch_length              OK       field in base class                  defined: NXsource/bunch_length                                                             
    /entry/instrument/source_pump/bunch_length@units        TODO     attribute value                      implement                                                                                  
    /entry/instrument/source_pump/bunch_length@units        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/burst_distance            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/burst_distance            OK       field in base class                  not defined: NXsource/burst_distance                                                       
    /entry/instrument/source_pump/burst_distance@units      TODO     attribute value                      implement                                                                                  
    /entry/instrument/source_pump/burst_distance@units      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/burst_length              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/burst_length              OK       field in base class                  not defined: NXsource/burst_length                                                         
    /entry/instrument/source_pump/burst_length@units        TODO     attribute value                      implement                                                                                  
    /entry/instrument/source_pump/burst_length@units        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/frequency                 OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/frequency                 OK       field in base class                  defined: NXsource/frequency                                                                
    /entry/instrument/source_pump/frequency@units           TODO     attribute value                      implement                                                                                  
    /entry/instrument/source_pump/frequency@units           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/mode                      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/mode                      OK       field in base class                  defined: NXsource/mode                                                                     
    /entry/instrument/source_pump/name                      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/name                      OK       field in base class                  defined: NXsource/name                                                                     
    /entry/instrument/source_pump/number_of_bunches         OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/number_of_bunches         OK       field in base class                  defined: NXsource/number_of_bunches                                                        
    /entry/instrument/source_pump/number_of_bursts          OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/number_of_bursts          OK       field in base class                  not defined: NXsource/number_of_bursts                                                     
    /entry/instrument/source_pump/probe                     OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/probe                     OK       field in base class                  defined: NXsource/probe                                                                    
    /entry/instrument/source_pump/rms_jitter                OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/rms_jitter                OK       field in base class                  not defined: NXsource/rms_jitter                                                           
    /entry/instrument/source_pump/rms_jitter@units          TODO     attribute value                      implement                                                                                  
    /entry/instrument/source_pump/rms_jitter@units          OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/type                      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/source_pump/type                      OK       field in base class                  defined: NXsource/type                                                                     
    /entry/instrument/spatial_resolution                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/spatial_resolution                    OK       field in base class                  not defined: NXinstrument/spatial_resolution                                               
    /entry/instrument/spatial_resolution@units              TODO     attribute value                      implement                                                                                  
    /entry/instrument/spatial_resolution@units              OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/temporal_resolution                   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/instrument/temporal_resolution                   OK       field in base class                  not defined: NXinstrument/temporal_resolution                                              
    /entry/instrument/temporal_resolution@units             TODO     attribute value                      implement                                                                                  
    /entry/instrument/temporal_resolution@units             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/run_cycle                                        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/run_cycle                                        OK       field in base class                  defined: NXentry/run_cycle                                                                 
    /entry/sample                                           TODO     NeXus base class                     NXsample: more validations needed                                                          
    /entry/sample                                           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample                                           OK       group in base class                  defined: NXentry/sample                                                                    
    /entry/sample                                           OK       known NXDL                           NXsample: recognized NXDL specification                                                    
    /entry/sample                                           OK       NeXus base class                     NXsample: known NeXus base class                                                           
    /entry/sample                                           OK       NXDL field in data file              found: /entry/sample/name                                                                  
    /entry/sample                                           OK       NXDL field in data file              found: /entry/sample/pressure                                                              
    /entry/sample                                           OK       NXDL field in data file              found: /entry/sample/temperature                                                           
    /entry/sample                                           OK       NXDL field in data file              found: /entry/sample/thickness                                                             
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/changer_position                                                  
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/chemical_formula                                                  
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/component                                                         
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/concentration                                                     
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/density                                                           
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/description                                                       
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/distance                                                          
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/electric_field                                                    
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/external_DAC                                                      
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/magnetic_field1                                                   
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/mass                                                              
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/orientation_matrix                                                
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/path_length                                                       
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/path_length_window                                                
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/physical_form                                                     
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/point_group                                                       
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/preparation_date                                                  
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/relative_molecular_mass                                           
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/rotation_angle                                                    
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/sample_component1                                                 
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/sample_orientation                                                
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/scattering_length_density                                         
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/short_title                                                       
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/situation                                                         
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/space_group                                                       
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/stress_field                                                      
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/type                                                              
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/ub_matrix                                                         
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/unit_cell                                                         
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/unit_cell_abc                                                     
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/unit_cell_alphabetagamma                                          
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/unit_cell_class                                                   
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/unit_cell_volume                                                  
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/volume_fraction                                                   
    /entry/sample                                           OPTIONAL NXDL field in data file              not found: /entry/sample/x_translation                                                     
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/beam                                                          
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/environment                                                   
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/external_ADC                                                  
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/geometry                                                      
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/history                                                       
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/magnetic_field                                                
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/magnetic_field_env                                            
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/magnetic_field_log                                            
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/off_geometry                                                  
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/positioner                                                    
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/sample_component                                              
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/temperature_env                                               
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/temperature_log                                               
    /entry/sample                                           OPTIONAL NXDL group in data file              not found:  in /entry/sample/transmission                                                  
    /entry/sample@NX_class                                  OK       validItemName                        pattern: NX.+                                                                              
    /entry/sample@NX_class                                  OK       attribute value                      recognized NXDL base class: NXsample                                                       
    /entry/sample@NX_class                                  OK       known attribute                      known: NXsample@NX_class                                                                   
    /entry/sample/bias                                      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/bias                                      OK       field in base class                  not defined: NXsample/bias                                                                 
    /entry/sample/bias@target                               OK       attribute value                      found: @target=/entry/instrument/manipulator/sample_bias                                   
    /entry/sample/bias@units                                TODO     attribute value                      implement                                                                                  
    /entry/sample/chem_id_cas                               OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/chem_id_cas                               OK       field in base class                  not defined: NXsample/chem_id_cas                                                          
    /entry/sample/chemical_name                             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/chemical_name                             OK       field in base class                  not defined: NXsample/chemical_name                                                        
    /entry/sample/growth_method                             OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/growth_method                             OK       field in base class                  not defined: NXsample/growth_method                                                        
    /entry/sample/layer                                     OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/layer                                     OK       field in base class                  not defined: NXsample/layer                                                                
    /entry/sample/name                                      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/name                                      OK       field in base class                  defined: NXsample/name                                                                     
    /entry/sample/preparation_method                        OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/preparation_method                        OK       field in base class                  not defined: NXsample/preparation_method                                                   
    /entry/sample/pressure                                  OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/pressure                                  OK       field in base class                  defined: NXsample/pressure                                                                 
    /entry/sample/pressure@units                            TODO     attribute value                      implement                                                                                  
    /entry/sample/pressure@units                            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/purity                                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/purity                                    OK       field in base class                  not defined: NXsample/purity                                                               
    /entry/sample/state                                     OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/state                                     OK       field in base class                  not defined: NXsample/state                                                                
    /entry/sample/surface_orientation                       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/surface_orientation                       OK       field in base class                  not defined: NXsample/surface_orientation                                                  
    /entry/sample/temperature                               OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/temperature                               OK       field in base class                  defined: NXsample/temperature                                                              
    /entry/sample/temperature@target                        OK       attribute value                      found: @target=/entry/instrument/manipulator/sample_temperature                            
    /entry/sample/temperature@units                         TODO     attribute value                      implement                                                                                  
    /entry/sample/thickness                                 OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/thickness                                 OK       field in base class                  defined: NXsample/thickness                                                                
    /entry/sample/thickness@units                           TODO     attribute value                      implement                                                                                  
    /entry/sample/thickness@units                           OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/vendor                                    OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/sample/vendor                                    OK       field in base class                  not defined: NXsample/vendor                                                               
    /entry/start_time                                       OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/start_time                                       OK       field in base class                  defined: NXentry/start_time                                                                
    /entry/start_time                                       OK       NXDL field                           NXarpes:start_time found                                                                   
    /entry/title                                            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*                                                           
    /entry/title                                            OK       field in base class                  defined: NXentry/title                                                                     
    /entry/title                                            OK       NXDL field                           NXarpes:title found                                                                        
    ======================================================= ======== ==================================== ===========================================================================================


    summary statistics
    ======== ===== =========================================================== =========
    status   count description                                                 (value)  
    ======== ===== =========================================================== =========
    OK       472   meets NeXus specification                                   100      
    NOTE     0     does not meet NeXus specification, but acceptable           75       
    WARN     0     does not meet NeXus specification, not generally acceptable 25       
    ERROR    0     violates NeXus specification                                -10000000
    TODO     88    validation not implemented yet                              0        
    UNUSED   0     optional NeXus item not used in data file                   0        
    COMMENT  0     comment from the punx source code                           0        
    OPTIONAL 326   allowed by NeXus specification, not identified              99       
            --                                                                         
    TOTAL    886                                                                        
    ======== ===== =========================================================== =========

    <finding>=99.591479 of 798 items reviewed
    NeXus definitions version: main
    ```

The output tables "findings" and "summary statistics" can be used to find error present in the NeXus file. As you can see, while the output is verbose and comprehensive, `punx` does not actually pick up on the issues that the [`pynxtools` validator finds](validate-nexus-files.md#validate_nexus).

You can just pass one of the logging levels to the `--report` flag to select for a subset of the report:

=== "Source"
    ```console
    punx validate --report ERROR src/pynxtools/data/201805_WSe2_arpes.nxs
    ```

=== "Result"

    ```console
    !!! WARNING: this program is not ready for distribution.

    data file: src/pynxtools/data/201805_WSe2_arpes.nxs
    NeXus definitions: main, dated 2025-08-14 04:24:42, sha=7ac3f9c2376bbe8c9c9c942652f0c9c3bfb065fe

    findings
    ======= ====== ==== ========
    address status test comments
    ======= ====== ==== ========
    ======= ====== ==== ========


    summary statistics
    ======== ===== =========================================================== =========
    status   count description                                                 (value)
    ======== ===== =========================================================== =========
    OK       472   meets NeXus specification                                   100
    NOTE     0     does not meet NeXus specification, but acceptable           75
    WARN     0     does not meet NeXus specification, not generally acceptable 25
    ERROR    0     violates NeXus specification                                -10000000
    TODO     88    validation not implemented yet                              0
    UNUSED   0     optional NeXus item not used in data file                   0
    COMMENT  0     comment from the punx source code                           0
    OPTIONAL 326   allowed by NeXus specification, not identified              99
            --
    TOTAL    886
    ======== ===== =========================================================== =========

    <finding>=99.591479 of 798 items reviewed
    ```

### Demo of `punx`

You can also invoke the help call for the validation API:

=== "Source"
    ```console
    punx validate --help
    ```

=== "Result"
    ```console
    !!! WARNING: this program is not ready for distribution.

    usage: punx validate [-h] [-f FILE_SET_NAME] [--report REPORT] infile

    positional arguments:
      infile                HDF5 or NXDL file name

    options:
      -h, --help            show this help message and exit
      -f FILE_SET_NAME, --file_set_name FILE_SET_NAME
                            NeXus NXDL file set (definitions) name for validation -- default=main
      --report REPORT       select which validation findings to report, choices:
                            COMMENT,ERROR,NOTE,OK,OPTIONAL,TODO,UNUSED,WARN (separate with comma if more
                            than one, do not use white space)
    ```

You can get a demonstration of `punx` by running:

=== "Source"
    ```console
    punx demo
    ```

=== "Result"
    ```
    console> punx validate C:\Users\USER\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\punx\data\writer_1_3.hdf5
    data file: C:\Users\USER\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\punx\data\writer_1_3.hdf5
    NeXus definitions: main, dated 2024-01-02 03:04:05, sha=xxxx21fxcef02xfbaa6x04e182e3d67dace7ef1b

    findings
    ============================ ======== ==================================== ==========================================================
    address                      status   test                                 comments
    ============================ ======== ==================================== ==========================================================
    /                            TODO     NeXus base class                     NXroot: more validations needed
    /                            OK       known NXDL                           NXroot: recognized NXDL specification
    /                            OK       NeXus base class                     NXroot: known NeXus base class
    /                            OK       NeXus default plot                   found by v3: /Scan/data/counts
    /                            OPTIONAL NXDL group in data file              not found:  in //entry
    /Scan                        TODO     NeXus base class                     NXentry: more validations needed
    /Scan                        OK       group in base class                  not defined: NXroot/Scan
    /Scan                        OK       known NXDL                           NXentry: recognized NXDL specification
    /Scan                        OK       NeXus base class                     NXentry: known NeXus base class
    /Scan                        OK       NXDL group in data file              found:  in /Scan/data
    /Scan                        NOTE     validItemName                        relaxed pattern: [a-zA-Z0-9_]([a-zA-Z0-9_.]*[a-zA-Z0-9_])?
    /Scan                        OPTIONAL NXDL field in data file              not found: /Scan/collection_description
    /Scan                        OPTIONAL NXDL field in data file              not found: /Scan/collection_identifier
    /Scan                        OPTIONAL NXDL field in data file              not found: /Scan/collection_time
    /Scan                        OPTIONAL NXDL field in data file              not found: /Scan/definition
    /Scan                        OPTIONAL NXDL field in data file              not found: /Scan/definition_local
    ...
    ...
    ...
    /Scan/data@signal            OK       known attribute                      known: NXdata@signal
    /Scan/data@signal            OK       value of @signal                     found: /Scan/data/counts
    /Scan/data@signal            OK       NeXus default plot v3, NXdata@signal correct default plot setup in /NXentry/NXdata
    /Scan/data@two_theta_indices TODO     attribute value                      implement
    /Scan/data@two_theta_indices OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*
    /Scan/data@two_theta_indices OK       known attribute                      unknown: NXdata@two_theta_indices
    /Scan/data/counts            OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*
    /Scan/data/counts            OK       field in base class                  not defined: NXdata/counts
    /Scan/data/counts@units      TODO     attribute value                      implement
    /Scan/data/counts@units      OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*
    /Scan/data/two_theta         OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*
    /Scan/data/two_theta         OK       field in base class                  not defined: NXdata/two_theta
    /Scan/data/two_theta@units   TODO     attribute value                      implement
    /Scan/data/two_theta@units   OK       validItemName                        strict pattern: [a-z_][a-z0-9_]*
    ============================ ======== ==================================== ==========================================================


    summary statistics
    ======== ===== =========================================================== =========
    status   count description                                                 (value)
    ======== ===== =========================================================== =========
    OK       35    meets NeXus specification                                   100
    NOTE     1     does not meet NeXus specification, but acceptable           75
    WARN     0     does not meet NeXus specification, not generally acceptable 25
    ERROR    0     violates NeXus specification                                -10000000
    TODO     7     validation not implemented yet                              0
    UNUSED   0     optional NeXus item not used in data file                   0
    COMMENT  0     comment from the punx source code                           0
    OPTIONAL 40    allowed by NeXus specification, not identified              99
            --
    TOTAL    83
    ======== ===== =========================================================== =========

    <finding>=99.144737 of 76 items reviewed
    NeXus definitions version: main

    console> punx tree C:\Users\rh83hixu\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\punx\data\writer_1_3.hdf5
    C:\Users\rh83hixu\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\punx\data\writer_1_3.hdf5 : NeXus data file
      Scan:NXentry
        @NX_class = "NXentry"
        data:NXdata
          @NX_class = "NXdata"
          @axes = "two_theta"
          @signal = "counts"
          @two_theta_indices = [0]
          counts:NX_INT32[31] = [1037, 1318, 1704, '...', 1321]
            @units = "counts"
          two_theta:NX_FLOAT64[31] = [17.92608, 17.92591, 17.92575, '...', 17.92108]
            @units = "degrees"
    ```

### Further notes

1. [More installation details](<https://punx.readthedocs.io/en/latest/install.html>)
2. [Other punx commands](<https://punx.readthedocs.io/en/latest/overview.html#>)
3. [Github project](<https://github.com/prjemian/punx>)

## `nexpy/nxvalidate`: A python API for validating NeXus file

This is a validation tool developed by the [`NeXpy` project](https://github.com/nexpy).

- [GitHub repository](https://github.com/nexpy/nxvalidate)

### Installation

The package can be installed via any Python package manager:

=== "uv"
    ```console
    uv pip install nxvalidate
    ```

=== "pip"

    ```console
    pip install nxvalidate
    ```

### Usage

After installation, you can invoke the help call from the command line:

=== "Source"
    ```console
    nxinspect --help
    ```

=== "Result"

    ```console
    usage: nxinspect [-h] [-f FILENAME] [-p PATH] [-a [APPLICATION]] [-b BASECLASS] [-d DEFINITIONS]
                 [-i] [-w] [-e] [-v]

    Inspects and validates NeXus files.

    options:
      -h, --help            show this help message and exit
      -f FILENAME, --filename FILENAME
                            name of the NeXus file to be validated
      -p PATH, --path PATH  path to group to be validated in the NeXus file
      -a [APPLICATION], --application [APPLICATION]
                            validate the NeXus file against its application definition
      -b BASECLASS, --baseclass BASECLASS
                            name of the base class to be listed
      -d DEFINITIONS, --definitions DEFINITIONS
                            path to the directory containing NeXus definitions
      -i, --info            output info messages in addition to warnings and errors
      -w, --warning         output warning and error messages (default)
      -e, --error           output errors
      -v, --version         show program's version number and exit
    ```

!!! info "NeXus definitions in `nxvalidate`"
    The `nxvalidate` package comes with a pre-defined set of NeXus definitions by itself. As of July 2025, only the official definitions from the NIAC repository are available (from release [v2024.02](https://github.com/nexusformat/definitions/releases/tag/v2024.02)).

    If you want to run the validation against a different set of NeXus definitions, you can specify their path using the `-d` flag in the validation.

### Validation in `nxvalidate`

You can start the validation by running

=== "Source"
    ```console
    nxinspect -f 201805_WSe2_arpes.nxs
    ```

=== "Result"

    ```console
    NXValidate
    ----------
    Filename: /home/user/fairmat/nomad-distro-dev/packages/pynxtools/src/pynxtools/data/201805_
    Path: /
    Definitions: /home/user/fairmat/nomad-distro-dev/.venv/lib/python3.12/site-packages/nxvalid
    NXroot: /
        "@nexusformat_version" is not defined as an attribute in NXroot
        NXentry: /entry
            Field: /entry/collection_time
                The field value is not a valid NX_FLOAT
            NXinstrument: /entry/instrument
                NXdetector: /entry/instrument/analyser
                    Field: /entry/instrument/analyser/acquisition_mode
                        The field value is not a member of the enumerated list
                    Field: /entry/instrument/analyser/amplifier_type
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/angles
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/contrast_aperture
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/data
                        The field has rank 3, should be 4
                        The field rank is 3, but the dimension index of "tof" = 4
                    Field: /entry/instrument/analyser/delays
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/detector_type
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/dispersion_scheme
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/energies
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/entrance_slit_setting
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/entrance_slit_shape
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/entrance_slit_size
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/extractor_voltage
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/field_aperture_x
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/field_aperture_y
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/lens_mode
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/magnification
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/pass_energy
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/projection
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/region_origin
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/region_size
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/sensor_count
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/sensor_size
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/time_per_channel
                        This field is not defined in NXdetector
                    Field: /entry/instrument/analyser/working_distance
                        This field is not defined in NXdetector
                NXbeam: /entry/instrument/beam_probe_0
                    Field: /entry/instrument/beam_probe_0/distance
                        The field value is not a valid NX_FLOAT
                    Field: /entry/instrument/beam_probe_0/photon_energy
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_probe_0/polarization_angle
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_probe_0/polarization_ellipticity
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_probe_0/pulse_duration
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_probe_0/size_x
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_probe_0/size_y
                        This field is not defined in NXbeam
                NXbeam: /entry/instrument/beam_pump_0
                    Field: /entry/instrument/beam_pump_0/average_power
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_pump_0/center_wavelength
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_pump_0/distance
                        The field value is not a valid NX_FLOAT
                    Field: /entry/instrument/beam_pump_0/fluence
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_pump_0/photon_energy
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_pump_0/polarization_angle
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_pump_0/polarization_ellipticity
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_pump_0/pulse_duration
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_pump_0/pulse_energy
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_pump_0/size_x
                        This field is not defined in NXbeam
                    Field: /entry/instrument/beam_pump_0/size_y
                        This field is not defined in NXbeam
                Field: /entry/instrument/energy_resolution
                    This field is not defined in NXinstrument
                NXpositioner: /entry/instrument/manipulator
                    Field: /entry/instrument/manipulator/pos_x1
                        This field is not defined in NXpositioner
                    Field: /entry/instrument/manipulator/pos_x2
                        This field is not defined in NXpositioner
                    Field: /entry/instrument/manipulator/pos_y
                        This field is not defined in NXpositioner
                    Field: /entry/instrument/manipulator/pos_z1
                        This field is not defined in NXpositioner
                    Field: /entry/instrument/manipulator/pos_z2
                        This field is not defined in NXpositioner
                    Field: /entry/instrument/manipulator/pos_z3
                        This field is not defined in NXpositioner
                    Field: /entry/instrument/manipulator/sample_bias
                        This field is not defined in NXpositioner
                    Field: /entry/instrument/manipulator/sample_temperature
                        This field is not defined in NXpositioner
                    Field: /entry/instrument/manipulator/type
                        This field is not defined in NXpositioner
                NXmonochromator: /entry/instrument/monochromator
                    Field: /entry/instrument/monochromator/energy_error
                        This field is now deprecated. see https://github.com/nexus
                    NXslit: /entry/instrument/monochromator/slit
                        NXslit is an invalid class in NXmonochromator
                NXsource: /entry/instrument/source
                    Field: /entry/instrument/source/bunch_distance
                        The field value is not a valid NX_FLOAT
                    Field: /entry/instrument/source/bunch_length
                        The field value is not a valid NX_FLOAT
                    Field: /entry/instrument/source/burst_distance
                        This field is not defined in NXsource
                    Field: /entry/instrument/source/burst_length
                        This field is not defined in NXsource
                    Field: /entry/instrument/source/burst_number_end
                        This field is not defined in NXsource
                    Field: /entry/instrument/source/burst_number_start
                        This field is not defined in NXsource
                    Field: /entry/instrument/source/current
                        The field value is not a valid NX_FLOAT
                    Field: /entry/instrument/source/energy
                        The field value is not a valid NX_FLOAT
                    Field: /entry/instrument/source/frequency
                        The field value is not a valid NX_FLOAT
                    Field: /entry/instrument/source/mode
                        The field value is not a member of the enumerated list
                    Field: /entry/instrument/source/number_of_bursts
                        This field is not defined in NXsource
                    Field: /entry/instrument/source/type
                        The field value is not a member of the enumerated list
                NXsource: /entry/instrument/source_pump
                    Field: /entry/instrument/source_pump/bunch_distance
                        The field value is not a valid NX_FLOAT
                    Field: /entry/instrument/source_pump/bunch_length
                        The field value is not a valid NX_FLOAT
                    Field: /entry/instrument/source_pump/burst_distance
                        This field is not defined in NXsource
                    Field: /entry/instrument/source_pump/burst_length
                        This field is not defined in NXsource
                    Field: /entry/instrument/source_pump/frequency
                        The field value is not a valid NX_FLOAT
                    Field: /entry/instrument/source_pump/mode
                        The field value is not a member of the enumerated list
                    Field: /entry/instrument/source_pump/number_of_bursts
                        This field is not defined in NXsource
                    Field: /entry/instrument/source_pump/probe
                        The field value is not a member of the enumerated list
                    Field: /entry/instrument/source_pump/rms_jitter
                        This field is not defined in NXsource
                    Field: /entry/instrument/source_pump/type
                        The field value is not a member of the enumerated list
                Field: /entry/instrument/spatial_resolution
                    This field is not defined in NXinstrument
                Field: /entry/instrument/temporal_resolution
                    This field is not defined in NXinstrument
            NXsample: /entry/sample
                Link: /entry/sample/bias
                    This field is not defined in NXsample
                Field: /entry/sample/chem_id_cas
                    This field is not defined in NXsample
                Field: /entry/sample/chemical_name
                    This field is not defined in NXsample
                Field: /entry/sample/growth_method
                    This field is not defined in NXsample
                Field: /entry/sample/layer
                    This field is not defined in NXsample
                Field: /entry/sample/preparation_method
                    This field is not defined in NXsample
                Field: /entry/sample/pressure
                    The field rank is 0, but the dimension index of "n_pField" = 1
                Field: /entry/sample/purity
                    This field is not defined in NXsample
                Field: /entry/sample/state
                    This field is not defined in NXsample
                Field: /entry/sample/surface_orientation
                    This field is not defined in NXsample
                Link: /entry/sample/temperature
                    The field value is not a valid NX_FLOAT
                Field: /entry/sample/vendor
                    This field is not defined in NXsample

    Total number of warnings: 87
    Total number of errors: 7
    ```
  
Again, the output log is rather verbose. `nxvalidate` correctly picks up on undocumented concepts ("this field is not defined in ...") as well as values not matching enumerated items. Additionally, the wrong use of dimensions is documented.

`nxvalidate` also comes with a selection between a validator for application definitions and one for base classes. By default, the validator checks against concepts defined in the given application definitions and also against those in the used base classes. By using the `-a` flag, the file is _only_ validated against concepts defined directly in the application definition.

=== "Source"
    ```console
    nxinspect -a -f 201805_WSe2_arpes.nxs
    ```

=== "Result"

    ```console
    nxinspect -f src/pynxtools/data/201805_WSe2_arpes.nxs -a

    NXValidate
    ----------
    Filename: /home/user/fairmat/nomad-distro-dev/packages/pynxtools/src/pynxtools/data/201805_
    Entry: /entry
    Application Definition: NXarpes
    NXDL File: /home/user/fairmat/nomad-distro-dev/.venv/lib/python3.12/site-packages/nxvalidat
            Group: NXsource
            Field: /entry/instrument/source_pump/probe
                The field value is not a member of the enumerated list
        Group: analyser: NXdetector
            Field: /entry/instrument/analyser/entrance_slit_setting
                Units of NX_ANY not specified
            Field: /entry/instrument/analyser/sensor_size
                The field has size (2,), should be 2
            Field: /entry/instrument/analyser/region_origin
                The field has size (2,), should be 2
            Field: /entry/instrument/analyser/region_size
                The field has size (2,), should be 2

    Total number of warnings: 4
    Total number of errors: 1
    ```

If you want to see the contents of a given base class, the `-b` option can be used:

=== "Source"
    ```console
    nxinspect -f src/pynxtools/data/201805_WSe2_arpes.nxs -b NXsample
    ```

=== "Result"

    ```console
    NXValidate
    ----------
    Valid components of the NXsample base class
    NXDL File: /home/user/fairmat/nomad-distro-dev/.venv/lib/python3.12/site-packages/nxvalidat
    Allowed Attributes
        @default
    Allowed Groups
        geometry: {'@type': 'NXgeometry', '@deprecated': 'Use the field `depends_on` and :ref:`NXtr
        NXbeam: {}
        NXsample_component: {}
        transmission: {'@type': 'NXdata'}
        temperature_log: {'@type': 'NXlog', '@deprecated': 'use ``temperature``, see: https://githu
        temperature_env: {'@type': 'NXenvironment'}
        magnetic_field: {'@type': 'NXlog'}
        magnetic_field_log: {'@type': 'NXlog', '@deprecated': 'use ``magnetic_field``, see: https:/
        magnetic_field_env: {'@type': 'NXenvironment'}
        external_ADC: {'@type': 'NXlog'}
        NXpositioner: {}
        NXoff_geometry: {'@minOccurs': '0'}
        NXtransformations: {}
        NXcollection: {}
        NXdata: {}
        NXgeometry: {}
        NXlog: {}
        NXnote: {}
        NXparameters: {}
        GROUPNAME_log[NXlog]: {'@nameType': 'partial'}
    Allowed Fields
        name: {}
        chemical_formula: {}
        temperature: {'@type': 'NX_FLOAT', '@units': 'NX_TEMPERATURE'}
            dimensions: {'rank': 'anyRank', 'dim': {1: 'n_Temp'}}
        electric_field: {'@type': 'NX_FLOAT', '@units': 'NX_VOLTAGE'}
            dimensions: {'dim': {1: 'n_eField'}}
            attribute: {'direction': {'enumeration': ['x', 'y', 'z']}}
        magnetic_field: {'@type': 'NX_FLOAT', '@units': 'NX_ANY'}
            dimensions: {'dim': {1: 'n_mField'}}
            attribute: {'direction': {'enumeration': ['x', 'y', 'z']}}
        stress_field: {'@type': 'NX_FLOAT', '@units': 'NX_ANY'}
            dimensions: {'dim': {1: 'n_sField'}}
            attribute: {'direction': {'enumeration': ['x', 'y', 'z']}}
        pressure: {'@type': 'NX_FLOAT', '@units': 'NX_PRESSURE'}
            dimensions: {'dim': {1: 'n_pField'}}
        changer_position: {'@type': 'NX_INT', '@units': 'NX_UNITLESS'}
        unit_cell_abc: {'@type': 'NX_FLOAT', '@units': 'NX_LENGTH'}
            dimensions: {'dim': {1: '3'}}
        unit_cell_alphabetagamma: {'@type': 'NX_FLOAT', '@units': 'NX_ANGLE'}
            dimensions: {'dim': {1: '3'}}
        unit_cell: {'@type': 'NX_FLOAT', '@units': 'NX_LENGTH'}
            dimensions: {'rank': '2', 'dim': {1: 'n_comp', 2: '6'}}
        unit_cell_volume: {'@type': 'NX_FLOAT', '@units': 'NX_VOLUME'}
            dimensions: {'rank': '1', 'dim': {1: 'n_comp'}}
        sample_orientation: {'@type': 'NX_FLOAT', '@units': 'NX_ANGLE'}
            dimensions: {'rank': '1', 'dim': {1: '3'}}
        orientation_matrix: {'@type': 'NX_FLOAT'}
            dimensions: {'rank': '3', 'dim': {1: 'n_comp', 2: '3', 3: '3'}}
        ub_matrix: {'@type': 'NX_FLOAT'}
            dimensions: {'rank': '3', 'dim': {1: 'n_comp', 2: '3', 3: '3'}}
        mass: {'@type': 'NX_FLOAT', '@units': 'NX_MASS'}
            dimensions: {'rank': '1', 'dim': {1: 'n_comp'}}
        density: {'@type': 'NX_FLOAT', '@units': 'NX_MASS_DENSITY'}
            dimensions: {'rank': '1', 'dim': {1: 'n_comp'}}
        relative_molecular_mass: {'@type': 'NX_FLOAT', '@units': 'NX_MASS'}
            dimensions: {'rank': '1', 'dim': {1: 'n_comp'}}
        type: {}
            enumeration: ['sample', 'sample+can', 'can', 'sample+buffer', 'buffer', 'calibration sa
        situation: {}
            enumeration: ['air', 'vacuum', 'inert atmosphere', 'oxidising atmosphere', 'reducing at
        description: {}
        preparation_date: {'@type': 'NX_DATE_TIME'}
        component: {}
            dimensions: {'rank': '1', 'dim': {1: 'n_comp'}}
        sample_component: {}
            dimensions: {'rank': '1', 'dim': {1: 'n_comp'}}
            enumeration: ['sample', 'can', 'atmosphere', 'kit']
        concentration: {'@type': 'NX_FLOAT', '@units': 'NX_MASS_DENSITY'}
            dimensions: {'rank': '1', 'dim': {1: 'n_comp'}}
        volume_fraction: {'@type': 'NX_FLOAT'}
            dimensions: {'rank': '1', 'dim': {1: 'n_comp'}}
        scattering_length_density: {'@type': 'NX_FLOAT', '@units': 'NX_SCATTERING_LENGTH_DENSITY'}
            dimensions: {'rank': '1', 'dim': {1: 'n_comp'}}
        unit_cell_class: {}
            enumeration: ['triclinic', 'monoclinic', 'orthorhombic', 'tetragonal', 'rhombohedral',
        space_group: {}
            dimensions: {'dim': {1: 'n_comp'}}
        point_group: {}
            dimensions: {'dim': {1: 'n_comp'}}
        path_length: {'@type': 'NX_FLOAT', '@units': 'NX_LENGTH'}
        path_length_window: {'@type': 'NX_FLOAT', '@units': 'NX_LENGTH'}
        thickness: {'@type': 'NX_FLOAT', '@units': 'NX_LENGTH'}
        external_DAC: {'@type': 'NX_FLOAT', '@units': 'NX_ANY'}
        short_title: {}
        rotation_angle: {'@type': 'NX_FLOAT', '@units': 'NX_ANGLE'}
        x_translation: {'@type': 'NX_FLOAT', '@units': 'NX_LENGTH'}
        distance: {'@type': 'NX_FLOAT', '@units': 'NX_LENGTH'}
        depends_on: {'@type': 'NX_CHAR'}
        FIELDNAME_set: {'@type': 'NX_NUMBER', '@nameType': 'partial'}
        FIELDNAME_errors: {'@type': 'NX_NUMBER', '@nameType': 'partial'}
        FIELDNAME_weights: {'@type': 'NX_NUMBER', '@nameType': 'partial'}
        FIELDNAME_mask: {'@type': 'NX_BOOLEAN', '@nameType': 'partial'}
    ```    

## Recommendations

We strongly recommend to use the [`validate_nexus`](./validate-nexus-files.md#validate_nexus) tool that is shipped with our `pynxtools` software, as it is likely to be the most complete and up-to-date solution around. However, if you want to use another tool to cross-check, the `nxvalidate` tool seems to be a good solution, as it picks up on all the issues that `validate_nexus` detects as well.
