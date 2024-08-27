# NeXus Validation Dev. Notes

# 1\. Overview of validation methods

nexusformat.org listed two programs for the verification and validataion of NeXus files:  
[https://manual.nexusformat.org/validation.htm](<https://manual.nexusformat.org/validation.html>)

1. nxvalidate

2. punx

## nxvalidate

[https://github.com/nexusformat/cnxvalidate](<https://github.com/nexusformat/cnxvalidate>)

### Pro:

1. FAIRmat and NIAC NeXus definiton can be used.

2. Easy to install with Linux

3. Points out some Errors with pynxtools-ellips created file - our fault?

### Con: 

1. Is C/C++ based

2. Not possible for Windows (cmake did not found the libxml2 library. Other libs were found after some work)

3. Last update 2 years ago - Repo is dead?

4. Unclear if every error is 100% a fault on our side - Florian was unsure/had some concerns about that.

## punx

[https://github.com/prjemian/punx](<https://github.com/prjemian/punx>) & [https://punx.readthedocs.io/en/latest/contents.html](<https://punx.readthedocs.io/en/latest/contents.html>)

### Pro:

1. Nice looking output and easy to use

2. Python code

3. Works on Linux and Windows

### Con:

1. Last update 1 year ago. Last commit 4month ago.

2. Still not finished.

3. Some nexus def. parts are not validated yet (see status "TODO" in "punx validate" output)

4. Can't use FAIRmat NeXus definitions. The command

```
punx install https://github.com/FAIRmat-NFDI/nexus_definitions/archive/refs/heads/fairmat
```

Does not allow me to install the .zip file. I as well modified the links in the python code, but there seem to be as well other check mechanisms.  
Hardconding the download link, resulted in the download of some NeXus files, but not all (e.g. NXoptical\_spectroscopy was not present (new) but as well NXopt was not present (old).

## pynxtools

Tools

1. read\_nexus

2. verify\_nexus ([https://github.com/FAIRmat-NFDI/pynxtools/pull/333/files](<https://github.com/FAIRmat-NFDI/pynxtools/pull/333/files>))

The first one only useful to check if the things in the file are "IN THE SCHEMA". Does not report missing things.

The second one was tested. Seems to be fine mostly, but reports some unexpected errors. Also does not report some errors, which were reportet by other tools.

# Summary: 

1. There are some tools

2. None fulfills all requirements

3. punx and cnxvalidate's development seemed to stopped?

4. Need own validation function?











# 2\. Examples from nxvalidate

## Example error from nxvaldiate for pynxtools-ellips generated ellipsometry nexus file:

```
(.py39) ron@hlp135:~/FAIRmat/WorkshopNeXusValid02/nxvalidate/cnxvalidate/build$ ./nxvalidate -l /home/ron/FAIRmat/WorkshopNeXusValid02/nxvalidate/nexus_definitions/ SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Data type mismatch, expected NX_BOOLEAN, got H5T_ENUM {
      H5T_STD_I8LE;
      "FALSE"            0;
      "TRUE"             1;
   }" nxdlPath=/NXentry/NXinstrument/NXlens_opt/data_correction sev=error dataPath=/entry/instrument/focussing_probes/data_correction dataFile=SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Required group missing" nxdlPath=/NXentry/NXinstrument/NXbeam sev=error dataPath=/entry/instrument dataFile=SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Required group missing" nxdlPath=/NXentry/NXinstrument/NXdetector sev=error dataPath=/entry/instrument dataFile=SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Data type mismatch, expected NX_BOOLEAN, got H5T_ENUM {
      H5T_STD_I8LE;
      "FALSE"            0;
      "TRUE"             1;
   }" nxdlPath=/NXentry/NXsample/backside_roughness sev=error dataPath=/entry/sample/backside_roughness dataFile=SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Required units attribute missing" nxdlPath=/NXentry/NXdata/measured_data sev=error dataPath=/entry/data_collection/measured_data dataFile=SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Data type mismatch, expected NX_BOOLEAN, got H5T_STRING {
      STRSIZE H5T_VARIABLE;
      STRPAD H5T_STR_NULLTERM;
      CSET H5T_CSET_UTF8;
      CTYPE H5T_C_S1;
   }" nxdlPath=/NXentry/NXidentifier/is_persistent sev=error dataPath=/entry/experiment_identifier/is_persistent dataFile=SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Required group missing" nxdlPath=/NXentry/NXdata sev=error dataPath=/entry dataFile=SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Required units attribute missing" nxdlPath=/NXentry/NXprocess/depolarization sev=error dataPath=/entry/derived_parameters/depolarization dataFile=SiO2onSi.ellips.nxs 
9 errors and 85 warnings found when validating SiO2onSi.ellips.nxs
```

### nxvalidate Errors:

1. "Data type mismatch, expected NX\_BOOLEAN" --> "NeXus interprets NX\_BOOLEAN differently than h5py. NeXus uses an integer of 1 byte for NX\_BOOLEAN. This is an int8 or uint8." --> [https://github.com/nexusformat/cnxvalidate/issues/34](<https://github.com/nexusformat/cnxvalidate/issues/34>)

2. Required group missing for "NXbeam" and "NXdetector". Probem with "exists: [min, 1, max, infty]"???

3. "Required units attribute missing" for entry/data\_collection/measured\_data --> ??? unclear. Units are assigned.

4. "Required group missing" for /entry ---> ?



### nxvalidate Warnings:

I think warnings can be evoked by: (-t in front of the NeXus file):

```
~/FAIRmat/WorkshopNeXusValid02/nxvalidate/cnxvalidate/build$ ./nxvalidate -l /home/ron/FAIRmat/WorkshopNeXusValid02/nxvalidate/nexus_definitions/ -t SiO2onSi.ellips.nxs
```

Most of the warnings are not critical at all. Not sure if this is helpful at all:

here are some examples of the "messages" of the warnings:

1. "Optional group missing"

2. "Optional field missing"

3. "Optional attribute units missing"

4. "Validating field"

5. "Validating group"

6. "Additional base class dataset name found"

7. "Additional base class dataset address found"

8. "Unknown dataset wavelength\_spectrum found"

9. "Additional base class group notes of type NXnote found"

10. "Additional base class group environment\_sample of type NXenvironment found"




# 3\. Testing different Validation outputs for a pynxtools-ellipsometry generated file.


## verify_nexus from pynxtools:
` verify_nexus SiO2onSi.ellips.nxs`

```
WARNING: Field /entry/data_collection/Delta_50deg/@units written without documentation.
WARNING: Field /entry/data_collection/Delta_50deg_errors/@units written without documentation.
WARNING: Field /entry/data_collection/Delta_60deg/@units written without documentation.
WARNING: Field /entry/data_collection/Delta_60deg_errors/@units written without documentation.
WARNING: Field /entry/data_collection/Delta_70deg/@units written without documentation.
WARNING: Field /entry/data_collection/Delta_70deg_errors/@units written without documentation.
WARNING: Field /entry/data_collection/Psi_50deg/@units written without documentation.
WARNING: Field /entry/data_collection/Psi_50deg_errors/@units written without documentation.
WARNING: Field /entry/data_collection/Psi_60deg/@units written without documentation.
WARNING: Field /entry/data_collection/Psi_60deg_errors/@units written without documentation.
WARNING: Field /entry/data_collection/Psi_70deg/@units written without documentation.
WARNING: Field /entry/data_collection/Psi_70deg_errors/@units written without documentation.
WARNING: Missing attribute: "/ENTRY/DATA/@axes"
WARNING: Missing attribute: "/ENTRY/DATA/@signal"
Invalid: The entry `entry` in file `SiO2onSi.ellips.nxs` is NOT a valid file according to the `NXellipsometry` application definition.
```
_Total 14 Errors_
_Total 3 Errors - without documentation_
1. Psi+Delta with Unit+Errors written without doc.
2. Data @axes + @signal. May not find NXdata? Attributes are present in .nxs file.
3. entry not valid in NXellips.

## read_nexus from pynxtools:
`read_nexus -f SiO2onSi.ellips.nxs > read_nexus_output_file.txt`
```
NXellipsometry.nxdl.xml:/ENTRY/data_collection/data_software
NXprogram.nxdl.xml:
DEBUG: @url - IS NOT IN SCHEMA
####################################################
NXellipsometry.nxdl.xml:/ENTRY/definition
NXoptical_spectroscopy.nxdl.xml:/ENTRY/definition
NXentry.nxdl.xml:/definition
DEBUG: @url - IS NOT IN SCHEMA
####################################################
DEBUG: ===== GROUP (//entry/instrument/software_RC2 [NXellipsometry::/NXentry/NXinstrument/software_RC2]): <HDF5 group "/entry/instrument/software_RC2" (1 members)>
DEBUG: classpath: ['NXentry', 'NXinstrument']
DEBUG: NOT IN SCHEMA
####################################################
DEBUG: ===== FIELD (//entry/instrument/software_RC2/program): <HDF5 dataset "program": shape (), type "|O">
DEBUG: value: b'CompleteEASE' 
DEBUG: classpath: ['NXentry', 'NXinstrument']
DEBUG: NOT IN SCHEMA
####################################################
DEBUG: ===== ATTRS (//entry/instrument/software_RC2/program@url)
DEBUG: value: https://www.jawoollam.com/ellipsometry-software/completeease 
DEBUG: classpath: ['NXentry', 'NXinstrument']
DEBUG: NOT IN SCHEMA
####################################################
DEBUG: ===== ATTRS (//entry/instrument/software_RC2/program@version)
DEBUG: value: 6.37 
DEBUG: classpath: ['NXentry', 'NXinstrument']
DEBUG: NOT IN SCHEMA
####################################################
```
_Total 6 Errors_
1. @url. Changing to @URL could fix this maybe.
2. Software_RC2 not detected as NXprogram. This is indeed not assigned.

## nxnvalidate from cnxvalidate:
`PATH_TO_NX_VALIDATE_EXE/nxvalidate -l PATH_TO_FAIRMAT_NEXUS_DEF/nexus_definitions/ PATH_TO_NEXUS_FILE/SiO2onSi.ellips.nxs`
```
definition=NXellipsometry.nxdl.xml message="Data type mismatch, expected NX_BOOLEAN, got H5T_ENUM {      H5T_STD_I8LE;      "FALSE"            0;      "TRUE"             1;   }" nxdlPath=/NXentry/NXinstrument/NXlens_opt/data_correction sev=error dataPath=/entry/instrument/focussing_probes/data_correction dataFile=/home/ron/GitPynxtoolsValidation/nexus_files/SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Required group missing" nxdlPath=/NXentry/NXinstrument/NXbeam sev=error dataPath=/entry/instrument dataFile=/home/ron/GitPynxtoolsValidation/nexus_files/SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Required group missing" nxdlPath=/NXentry/NXinstrument/NXdetector sev=error dataPath=/entry/instrument dataFile=/home/ron/GitPynxtoolsValidation/nexus_files/SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Data type mismatch, expected NX_BOOLEAN, got H5T_ENUM {      H5T_STD_I8LE;      "FALSE"            0;      "TRUE"             1;   }" nxdlPath=/NXentry/NXsample/backside_roughness sev=error dataPath=/entry/sample/backside_roughness dataFile=/home/ron/GitPynxtoolsValidation/nexus_files/SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Required units attribute missing" nxdlPath=/NXentry/NXdata/measured_data sev=error dataPath=/entry/data_collection/measured_data dataFile=/home/ron/GitPynxtoolsValidation/nexus_files/SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Data type mismatch, expected NX_BOOLEAN, got H5T_STRING {      STRSIZE H5T_VARIABLE;      STRPAD H5T_STR_NULLTERM;      CSET H5T_CSET_UTF8;      CTYPE H5T_C_S1;   }" nxdlPath=/NXentry/NXidentifier/is_persistent sev=error dataPath=/entry/experiment_identifier/is_persistent dataFile=/home/ron/GitPynxtoolsValidation/nexus_files/SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Required group missing" nxdlPath=/NXentry/NXdata sev=error dataPath=/entry dataFile=/home/ron/GitPynxtoolsValidation/nexus_files/SiO2onSi.ellips.nxs 
definition=NXellipsometry.nxdl.xml message="Required units attribute missing" nxdlPath=/NXentry/NXprocess/depolarization sev=error dataPath=/entry/derived_parameters/depolarization dataFile=/home/ron/GitPynxtoolsValidation/nexus_files/SiO2onSi.ellips.nxs 
9 errors and 85 warnings found when validating /home/ron/GitPynxtoolsValidation/nexus_files/SiO2onSi.ellips.nxs
```
_Total 8 or 9 Errors_
1. Datatype mismatch for Bools: "H5T_STRING" or "H5T_ENUM" instead of "NX_BOOLEAN". In NXlens_opt, backside_roughness and is_persistent.
2. NXbeam + NXdetector: Has a problem with "  exists: [min, 1, max, infty]"
3. "/NXentry/NXdata/measured_data". Units are missing (unit should be NX_ANY).
4. It does not find the NXdata (in this file it is at /entry/data_collection/).
5. Depolarization is not assigned the unit NX_unitless.


## validate from punx:
`punx validate SiO2onSi.ellips.nxs`
Not possible, as only the NIAC NeXus definitoon can right now be used as reference. Did not found out if `punx install` is functional to install the FAIRmat NeXus definition.


# Summary
| Error Message | origin | Error in .nxs file? | Error in validation tool? | 
| ---------------- | ---| ------------------------ |  ------------------------ |
| unit + error without doc    | verify_nexus | ?   | ?   |
| no @signal @axes for NXdata | verify_nexus | no  | yes |
| entry not valid in NXellips | verify_nexus | ?   | ?   |
| @url error                    | read_nexus | no  | yes |
| Software_RC2 no NXprogram     | read_nexus | yes | no  |
| Bool Data types               | nxvalidate | ?   | ?   |
| exists: [min, 1, max, infty]  | nxvalidate | no  | yes |
| Unit missing for measured_data| nxvalidate | yes | no  |
| NXdata not present            | nxvalidate | no  | yes |
| No unit for depolarization    | nxvalidate | yes | no  |


### NOTE ###
Only the nxvalidate method seems to point out completely missing required concepts.

I tested this with an empty NeXus file, in which only the "definition" was given.






# 4\. Installation Notes

## cnxvalidate installation on Ubuntu 22.04

These commands install nxvaldiate on a fresh Ubuntu 22.04 system (tested with Linux running from USB stick).

```
sudo apt-get update
sudo apt-get install git
sudo apt-get install build-essential
sudo add-apt-repository universe
sudo apt-get install libhdf5-serial-dev
sudo apt-get -y install pkg-config
sudo apt upgrade -y
sudo apt-get -y install cmake
sudo apt-get install libxml2-dev

mkdir nexusvalidate
cd nexusvalidate
git clone https://github.com/nexusformat/cnxvalidate.git
cd cnxvalidate/
mkdir build
cd build/
cmake ../
make
```

# cnxvalidate installation on windows:

## -- CMAKE

[https://cmake.org/download/](<https://cmake.org/download/>)

\--> [cmake-3.30.2-windows-x86\_64.msi](<https://github.com/Kitware/CMake/releases/download/v3.30.2/cmake-3.30.2-windows-x86_64.msi>)

Install with .msi

## -- HDF5

Download **hdf5-1.14.4-2-win-vs2022\_**[**cl.zip**](<http://cl.zip>)** from **[https://www.hdfgroup.org/downloads/hdf5/](<https://www.hdfgroup.org/downloads/hdf5/>)

unzip the .zip file

put the file into the folder

```
C:\hdf5
```

(can be named differently, but no spaces are allowed for this path)

```
set PATH=%PATH%;C:\your\path\here\
```

## -- libiconv

[https://github.com/vovythevov/libiconv-cmake](<https://github.com/vovythevov/libiconv-cmake>)

```
git clone
```

cd to downloaded directory

```
mkdir build
cd build
cmake ..
```

-- XML2

??? Unsolved...



