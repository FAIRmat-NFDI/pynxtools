# The shows the example of testing NeXus files with validation methods

There are [different methods](validate-nexus-file.md), which can be used for file validation.

- pynxtools (verify_nexus, read_nexus)
- nxvalidate
- punx

Here some examples are shown for the respective methods, by using a pynxtools-ellips generated NeXus file. This generated file already contained some level of validation, as a generated and filled template for this NeXus application definition was used.


# 1. Example from pynxtools read_nexus function

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

# 2. Example from pynxtools verify_nexus function

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


# 3. Example from nxvalidate

``PATH_TO_NX_VALIDATE_EXE/nxvalidate -l PATH_TO_FAIRMAT_NEXUS_DEF/nexus_definitions/ PATH_TO_NEXUS_FILE/SiO2onSi.ellips.nxs`
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

## nxvalidate Errors:

1. "Data type mismatch, expected NX\_BOOLEAN" --> "NeXus interprets NX\_BOOLEAN differently than h5py. NeXus uses an integer of 1 byte for NX\_BOOLEAN. This is an int8 or uint8." --> [https://github.com/nexusformat/cnxvalidate/issues/34](<https://github.com/nexusformat/cnxvalidate/issues/34>)

2. Required group missing for "NXbeam" and "NXdetector". Problem with NeXus requirement as given in the .yaml file by: "exists: [min, 1, max, infty]"?

3. "Required units attribute missing" for entry/data\_collection/measured\_data --> ? unclear. Units are assigned in NeXus file.

4. "Required group missing" for /entry ---> ? unclear.


## nxvalidate Warnings:

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






# 4. Example from punx
`punx validate SiO2onSi.ellips.nxs`
Not possible, as only the NIAC NeXus definition can right now be used as reference. Unclear if the `punx install` functionality is working or still developed.


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

I tested this with an empty NeXus file, in which only the "definition" was given (NXellipsometry and NXraman).






