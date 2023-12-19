# Troubleshooting Guide

### If you don't find a solution here, please make a new [Github Issue](https://github.com/FAIRmat-NFDI/pynxtools/issues/new?template=bug.yaml).

<br/>

## Module import error

```python
ImportError: cannot import name 'get_nexus_version' from 'pynxtools' (unknown location)
```

This is, unfortunately, expected behavior.  The Python import mechanism will first look for a folder with the package name in the current working directory. If it finds a folder named `pynxtools`, it will try to import from there. In this case we have the cloned repo folder with the same name, `pynxtools`. Python tries to import from this folder but the code resides in `pynxtools/pynxtools`.

### Solution

If you are working in a directory containing the repo folder, `pynxtools`, rename this repo folder to `pynxtools2` so your current directory looks like this:

```
.
├── pynxtools2                    # Renamed repo folder
│   ├── pynxtools          # Actual module code is in here
│   ├── tests
│   └── ...
└── my_code_imports_pynxtools.py
```

Then **reinstall the package** and your import will work.

### Steps to reproduce

```
git clone --recurse-submodules https://github.com/FAIRmat-NFDI/pynxtools.git
cd pynxtools
pip install -e .
cd ..
```

