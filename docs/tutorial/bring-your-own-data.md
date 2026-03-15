# Day 2 — Bring your own data

**Duration:** ~3 hours (self-paced, individual support)

**Goal:** Apply yesterday's MultiFormatReader pattern to your own instrument
data and produce a validated NeXus file.

**What to bring:** one or more data files from your instrument.

---

## The core idea — always the same three steps

No matter what format your data comes in, you always do the same three things:

```
Step A  Read your file(s) into flat Python dicts on self
Step B  Write a config file that maps dict keys → NeXus paths
Step C  Run the converter and fix validation errors
```

The only part that changes between techniques and formats is **Step A** — the
reading logic.  Steps B and C are identical to Day 1.

---

## Step 1 — Know your format (~30 min)

Before writing any reader code, understand what you are working with.

### Identify your format

| Format | Typical extensions | How to recognize |
|---|---|---|
| HDF5 / NeXus | `.h5`, `.hdf5`, `.nxs` | Binary; starts with `\x89HDF` |
| HDF5 (instrument brand) | `.h5m`, `.hsp`, `.he5`, … | Same magic bytes; vendor-specific internal layout |
| VAMAS | `.vms`, `.vamas` | First line: `VAMAS Surface Chemical Analysis` |
| Igor Pro wave | `.ibw` | Binary with `IGOR` header |
| CSV / TSV | `.csv`, `.txt`, `.dat`, `.asc` | Human-readable columns |
| JSON | `.json` | `{` or `[` as first non-whitespace character |
| YAML | `.yaml`, `.yml` | Key-value pairs with indentation |
| NetCDF | `.nc`, `.cdf`, `.netcdf` | Binary; readable with `netCDF4` or `xarray` |
| TIFF (detector images) | `.tiff`, `.tif` | Binary image; use `tifffile` or `PIL` |

---

## Step 2 — Read your file into a flat dict (~45 min)

Pick the section below that matches your format.
The goal in every case: populate `self.data` (or `self.hdf5_data`) with a flat
dict of `"path/to/quantity"` → value.

---

### Format: HDF5 (any vendor)

This is the same recursive reader from Day 1.  It works for **any** HDF5 file —
vendor-specific layouts, NeXus files, everything.

```python
import h5py

def handle_hdf5_file(self, file_path: str) -> dict[str, Any]:
    def _recurse(group, path=""):
        result = {}
        for key, item in group.items():
            full = f"{path}/{key}" if path else key
            if isinstance(item, h5py.Group):
                result.update(_recurse(item, full))
            elif isinstance(item, h5py.Dataset):
                result[full] = item[()]
        # also capture group-level attributes
        for attr_key, attr_val in group.attrs.items():
            result[f"{path}/@{attr_key}" if path else f"@{attr_key}"] = attr_val
        return result

    with h5py.File(file_path, "r") as hdf:
        self.hdf5_data = _recurse(hdf)
    return {}
```

After running, print the keys:

```python
r.handle_hdf5_file("your_file.h5")
for k in sorted(r.hdf5_data):
    print(k)
```

Map what you see to what NXsimple (or your application definition) needs.

---

### Format: CSV / TSV / columnar text

```python
import numpy as np

def handle_csv_file(self, file_path: str) -> dict[str, Any]:
    # Adjust delimiter, skiprows, and encoding for your file
    data = np.genfromtxt(
        file_path,
        delimiter=",",    # "\t" for TSV, None for whitespace
        names=True,       # use first row as column names
        encoding="utf-8",
        skip_header=0,
    )
    self.data = {name: data[name] for name in data.dtype.names}
    return {}
```

Or with pandas (more flexible for messy headers):

```python
import pandas as pd

def handle_csv_file(self, file_path: str) -> dict[str, Any]:
    # Read metadata lines before the data block (if any)
    meta = {}
    data_start = 0
    with open(file_path) as f:
        for i, line in enumerate(f):
            if line.startswith("#"):
                key, _, value = line[1:].partition("=")
                meta[key.strip()] = value.strip()
            else:
                data_start = i
                break

    df = pd.read_csv(file_path, skiprows=data_start, comment="#")
    self.data = {col: df[col].to_numpy() for col in df.columns}
    self.data.update(meta)   # metadata from header lines
    return {}
```

---

### Format: VAMAS (`.vms`)

VAMAS is a common format for XPS and other surface science data.

```python
def handle_vamas_file(self, file_path: str) -> dict[str, Any]:
    try:
        from vamas import Vamas
    except ImportError:
        raise ImportError("pip install vamas")

    vms = Vamas(file_path)
    block = vms.blocks[0]   # first spectrum; iterate for multiple

    self.data = {
        "kinetic_energy":     block.x,
        "intensity":          block.y,
        "source_energy":      block.source_energy,
        "pass_energy":        block.analyser_pass_energy,
        "dwell_time":         block.signal_collection_time,
        "sample_id":          block.sample_id,
        "technique":          block.technique,
        "comment":            block.comment,
    }
    return {}
```

If you have multiple blocks (spectra), store them as a list and loop in
`get_entry_names` / `get_data`.


---

### Format: Igor Pro IBW (`.ibw`)

```python
import igor2.igorpy as igor

def handle_ibw_file(self, file_path: str) -> dict[str, Any]:
    wave = igor.load(file_path)
    self.data = {
        "data": wave.data,
        "note": wave.notes.decode() if wave.notes else "",
    }
    # axis scaling
    for dim, (offset, delta) in enumerate(zip(wave.sfA, wave.sfB)):
        n = wave.data.shape[dim]
        axis = offset + delta * np.arange(n)
        self.data[f"axis_{dim}"] = axis
    return {}
```

Or for JSON note format:

```python
import igor2.igorpy as igor
import json

def handle_ibw_file(self, file_path: str) -> dict[str, Any]:
    wave = igor.load(file_path)
    self.data = {"signal": wave.data}
    try:
        meta = json.loads(wave.notes.decode())
        for k, v in meta.items():
            self.data[f"meta/{k}"] = v
    except (json.JSONDecodeError, AttributeError):
        pass
    return {}
```
---

### Format: NetCDF (`.nc`)

```python
import xarray as xr

def handle_netcdf_file(self, file_path: str) -> dict[str, Any]:
    ds = xr.open_dataset(file_path)
    self.data = {}
    for var in ds.data_vars:
        self.data[var] = ds[var].values
    for coord in ds.coords:
        self.data[f"axis/{coord}"] = ds.coords[coord].values
    for attr_key, attr_val in ds.attrs.items():
        self.data[f"attrs/{attr_key}"] = attr_val
    return {}
```

---

### Format: TIFF / detector images

```python
 import tifffile

def handle_tiff_file(self, file_path: str) -> dict[str, Any]:
    with tifffile.TiffFile(file_path) as tif:
        data = tif.asarray()       # shape: (frames, height, width) or (H, W)
        meta = {}
        if tif.is_imagej:
            meta = tif.imagej_metadata or {}
        elif tif.pages[0].tags:
            for tag in tif.pages[0].tags.values():
                meta[tag.name] = tag.value

    self.data = {"detector/image": data}
    self.data.update({f"meta/{k}": v for k, v in meta.items()})
    return {}
```

---

### Format: Plain JSON / YAML

```python
import json, yaml   # yaml: pip install pyyaml

def handle_json_file(self, file_path: str) -> dict[str, Any]:
    with open(file_path) as f:
        raw = json.load(f)
    self.data = self._flatten(raw)
    return {}

def handle_yaml_data_file(self, file_path: str) -> dict[str, Any]:
    with open(file_path) as f:
        raw = yaml.safe_load(f)
    self.data = self._flatten(raw)
    return {}

def _flatten(self, d: dict, parent: str = "") -> dict:
    """Recursively flatten a nested dict into slash-separated keys."""
    result = {}
    for k, v in d.items():
        full = f"{parent}/{k}" if parent else k
        if isinstance(v, dict):
            result.update(self._flatten(v, full))
        else:
            result[full] = v
    return result
```

---

### Format: anything else — the fallback pattern

When nothing above fits, write a minimal parser that extracts the values you
need and stores them in `self.data`:

```python
def handle_my_format(self, file_path: str) -> dict[str, Any]:
    self.data = {}

    with open(file_path, "rb") as f:   # or "r" for text
        raw = f.read()

    # --- parse raw bytes / text here ---
    # e.g. use struct, regex, or your vendor's SDK
    # ---

    # Store whatever you extract:
    self.data["signal"] = ...
    self.data["energy_axis"] = ...
    self.data["sample_name"] = ...

    return {}
```

Then add the extension to `self.extensions` in `__init__`:

```python
self.extensions[".myext"] = self.handle_my_format
```

---

## Step 3 — Adapt the callbacks (~20 min)

Once `self.data` is populated the callbacks are trivial.

If you used a single `self.data` dict (not `self.hdf5_data`), update the
callback methods:

```python
def get_attr(self, key: str, path: str) -> Any:
    if self.data is None:
        return None
    value = self.data.get(path)
    # decode byte strings if needed
    if isinstance(value, bytes):
        return value.decode()
    return value

def get_eln_data(self, key: str, path: str) -> Any:
    if self.eln_data is None:
        return None
    return self.eln_data.get(key)

def get_data(self, key: str, path: str) -> Any:
    if self.data is None:
        return None
    value = self.data.get(path)
    if value is None:
        logger.warning(f"No data at path '{path}'.")
    return value
```

---

## Step 4 — Find your application definition (~20 min)

### Does one already exist?

Check the [NeXus application definitions](https://manual.nexusformat.org/classes/applications/index.html)
and installed `pynxtools` plugins:

| Technique | application definition | `pynxtools` plugin |
|---|---|---|
| XPS | `NXxps` | `pynxtools-xps` |
| ARPES / multi-photon | `NXmpes`, `NXmpes_arpes`, `NXarpes` | `pynxtools-mpes` |
| Raman | `NXraman` | `pynxtools-raman` |
| Ellipsometry | `NXellipsometry` | `pynxtools-ellips` |
| Electron microscopy | `NXem` | `pynxtools-em` |
| Atom probe | `NXapm` | — |
| IXS / canSAS | `NXcanSAS`, `NXiqproc` | — |
| Generic simple | `NXsimple` | this workshop |

Test whether the application definition is known:

```bash
dataconverter generate-template --nxdl NXmpes
```

### No application definition? Write a minimal one.

See [How-to > Write a NeXus application definition](../how-tos/nexus/write-an-application-definition.md).

Minimal skeleton:

```xml title="NXmytechnique.nxdl.xml"
<?xml version="1.0" encoding="UTF-8"?>
<definition xmlns="http://definition.nexusformat.org/nxdl/3.1"
            category="application" name="NXmytechnique"
            extends="NXobject" type="group">
    <doc>Application definition for my technique.</doc>
    <group type="NXentry">
        <field name="title"/>
        <field name="definition">
            <enumeration><item value="NXmytechnique"/></enumeration>
        </field>
        <group type="NXinstrument">
            <field name="name"/>
        </group>
        <group name="sample" type="NXsample">
            <field name="name"/>
        </group>
        <group name="data" type="NXdata"/>
    </group>
</definition>
```

Save it next to `reader.py` and point `pynxtools` at it by adding to your reader:

```python
@classmethod
def get_nxdl_root_and_path(cls, nxdl: str):
    import os, lxml.etree as ET
    local = os.path.join(os.path.dirname(__file__), f"{nxdl}.nxdl.xml")
    if os.path.exists(local):
        return ET.parse(local).getroot(), local
    return super().get_nxdl_root_and_path(nxdl)
```

---

## Step 5 — Write the config file (~40 min)

### Mapping checklist

```bash
dataconverter generate-template --nxdl <YOUR_NXDL> > template.txt
```

Work through the output line by line.  For each path, fill in the
config JSON with the right `@`-prefix:

| Where is the value? | Config value |
|---|---|
| `self.data["some/key"]` | `"@attrs:some/key"` |
| `self.eln_data["/ENTRY[entry]/..."]` | `"@eln"` |
| `self.data["signal_array"]` | `"@data:signal_array"` |
| Always the same literal | `"fixed string"` or `42` |
| Derived in `post_process` | `"@attrs:derived/my_value"` |

### Handling missing data gracefully

Prefix a config key with `!` if the whole parent group should be dropped
when the value is absent:

```json
{
  "/ENTRY/INSTRUMENT[instrument]/DETECTOR[detector]": {
    "!count_time": "@attrs:detector/count_time",
    "count_time/@units": "@attrs:detector/count_time_units"
  }
}
```

If `count_time` returns `None`, the entire `DETECTOR[detector]` group is
silently removed from the output instead of causing a validation error.

### Unit fields

NeXus requires units for every numeric field.  Options:

```json
{ "/ENTRY/data/energy/@units": "eV" }                          // hard-coded
{ "/ENTRY/data/energy/@units": "@attrs:data/energy_units" }    // from file
```

---

## Step 6 — Convert, validate, iterate (~20 min)

```bash
dataconverter \
    your_file.ext \
    eln_data.yaml \
    config_file.json \
    --reader <your-reader> \
    --nxdl <YOUR_NXDL> \
    --output output.nxs
```

Read the output messages:

- **ERROR** — required field missing → add to config
- **WARNING** — recommended field missing → add if possible
- **INFO** — optional field missing → safe to skip

Inspect the result:

```python
import h5py
with h5py.File("output.nxs", "r") as f:
    f.visititems(lambda n, o: print(n) if isinstance(o, h5py.Dataset) else None)
```

Repeat until no errors remain.

---

## Advanced patterns

### Multiple spectra / entries per file

```python
def get_entry_names(self) -> list[str]:
    """Return one entry name per spectrum in the file."""
    if self.data is None:
        return ["entry"]
    return [f"spectrum_{i}" for i in range(len(self.data["spectra"]))]
```

Then use wildcard keys in the config with `*`:

```json
{ "/ENTRY/data/*/signal": "@data:signal" }
```

### Unit conversion in a callback

```python
def get_attr(self, key: str, path: str) -> Any:
    value = self.data.get(path) if self.data else None
    if value is None:
        return None
    # Example: convert Celsius to Kelvin for temperature fields
    if "temperature" in key and "units" not in key:
        return float(value) + 273.15
    if isinstance(value, bytes):
        return value.decode()
    return value
```

### Derived quantities in `post_process`

```python
def post_process(self) -> None:
    """Compute quantities that depend on multiple raw values."""
    if not self.data:
        return
    import numpy as np
    x = self.data.get("energy")
    y = self.data.get("counts")
    if x is not None and y is not None:
        peak_idx = np.argmax(y)
        self.data["derived/peak_energy"] = x[peak_idx]
        self.data["derived/peak_energy_units"] = b"eV"
```

---

## Common errors and fixes

| Error / symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: <vendor lib>` | Library not installed | `pip install <library>` — see table above |
| `KeyError: 'some/path'` in callback | Path missing from `self.data` | Print `sorted(self.data.keys())` to find the right key |
| Required field missing in output | Config doesn't map it | Add the path to config file |
| `bytes` in output string field | h5py byte string | Add `.decode()` in the callback |
| Numeric value has wrong magnitude | Unit mismatch | Apply conversion in the callback |
| All `get_eln_data` return `None` | Wrong CONVERT_DICT | Print `self.eln_data.keys()` vs `key` argument |
| File opens but data looks wrong | Wrong dataset path | Print the full `self.data` dict and re-map |
| `struct.error` / garbage in binary file | Wrong offset or dtype | Check vendor documentation for byte layout |
| Validation passes but file looks incomplete | application definition has no required fields | Add required fields to the NXDL |

---

## Checklist before you leave

- [ ] `dataconverter` runs without errors on your own data
- [ ] All required fields in the application definition are present in `output.nxs`
- [ ] Units are set for every numeric field
- [ ] `reader.py` and `config_file.json` are committed to your repository
- [ ] You know which application definition matches your technique (or have written a minimal one)

---

## Further reading

- [How-to > Use the MultiFormatReader](../how-tos/pynxtools/use-multi-format-reader.md)
- [How-to > Build a plugin](../how-tos/pynxtools/build-a-plugin.md)
- [How-to > Test your reader](../how-tos/pynxtools/using-pynxtools-test-framework.md)
- [Tutorial > Write your first application definition](../tutorial/writing-an-application-definition.md)
- [How-to > Write a NeXus application definition](../how-tos/nexus/write-an-application-definition.md)
(../how-tos/nexus/write-an-application definition.md)
- [Learn > The MultiFormatReader in depth](../learn/pynxtools/multi-format-reader.md)
- [Reference > FAIRmat-supported `pynxtools` plugins](../reference/plugins.md)
