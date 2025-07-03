
# Notes on cnxvalidate installation

This lists some notes for installation of nxvalidate on Ubuntu and Windows. For windows, the installation of the XML2 library was not successful. This should be possible, but could not reproduced yet.



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

## cnxvalidate installation on Windows:

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

## -- XML2

??? Unsolved...

Please create GitHub issue [here](https://github.com/FAIRmat-NFDI/pynxtools/issues/new) if you could solve this.

