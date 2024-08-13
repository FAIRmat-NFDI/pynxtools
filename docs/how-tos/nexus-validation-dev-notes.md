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

The second is in development. Has to be tested.

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













# 3\. Installation Notes

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



