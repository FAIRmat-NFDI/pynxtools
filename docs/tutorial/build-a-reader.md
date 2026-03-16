# Building your first pynxtools reader

This tutorial will guide you through writing your first `pynxtools` reader plugin.

## What should you should know before this tutorial?

- You should have a basic understanding of NeXus: see [Learn > NeXus -> A primer on NeXus](../learn/nexus/nexus-primer.md)
- You should have `pynxtools` installed: see the [Installation guide](./installation.md)

## What you will know at the end of this tutorial?

You will know

- how to use the template for `pynxtools` plugins
- how to set up a basic reader using the `MultiFormatReader`
- how to validate your NeXus file
- how to upload your NeXus file to NOMAD

---

## About this tutorial

**Duration:** ~3 hours

**Goal:** Convert a real instrument HDF5 file + an ELN YAML file into a validated NeXus/HDF5 output using a reader you write yourself.

---

## 0 — Before you start (~20 min)

### What is NeXus and why does it matter?

Scientific instruments produce data in dozens of incompatible formats. [NeXus](https://www.nexusformat.org/) is a community standard that defines a common structure for scientific data files so that tools, scripts, and databases can read them without format-specific code.

A NeXus file is an HDF5 file with an agreed-upon internal layout. The layout is defined by an **application definition** (NXDL file): an XML schema that defines which groups, fields, and attributes a valid file must contain. An application definition also defines how instances of concepts in a NeXus file should be named. Names frequently have a templated part, i.e., concepts names can be (partially) renamable.

`pynxtools` is the Python library that converts your raw data into a NeXus/HDF5 file and validates the result.

### The three-file pattern

Typically, a `pynxtools` reader plugin works with three types of input:

| File | What it is | Example |
|---|---|---|
| Instrument file | Raw data from the instrument | `mock_data.h5` |
| ELN file | Metadata you fill in yourself | `eln_data.yaml` |
| Config file | Mapping from your data to NeXus | `config_file.json` |

The **reader** reads the first two and the **config file** specifies the mapping.
You will write all three today.

### How the reader fits in

```
mock_data.h5   ──► handle_hdf5_file()  ──►  self.hdf5_data  ──┐
eln_data.yaml  ──► handle_eln_file()   ──►  self.eln_data   ──┤
                                                              │
config_file.json  ◄──────────────────────────────────────┘
       │
       │  "@attrs:some/hdf5/path"  ──►  get_attr(key, path)
       │  "@eln"                   ──►  get_eln_data(key, path)
       │  "@data:some/array"       ──►  get_data(key, path)
       │
       ▼
   output.nxs  (validated against NXsimple)
```

The `MultiFormatReader` base class handles all the plumbing.
**You only write the parts that know about your specific data.**

### Create your plugin

```bash
uv ip install cookiecutter
cookiecutter gh:FAIRmat-NFDI/pynxtools-plugin-template --checkout workshop
```

Enter these values:

| Prompt | Type | Value for today |
|---|---|---|
| `reader_name` | short lowercase name | `simple` |
| `supported_nxdl` | target appdef | `NXsimple` *(pre-filled)* |
| `short_description` | one-liner | `My first pynxtools reader` |
| All others | optional | press Enter to accept defaults |

Note that the template allows for many more optional features in your `pynxtools` plugin.
We are working on those in separate tutorials.

This creates the directory `pynxtools-simple/`. Enter it:

```bash
cd pynxtools-simple
```

### Install dependencies

```bash
# pynxtools from the workshop branch (contains NXsimple)
uv pip install "pynxtools @ git+https://github.com/FAIRmat-NFDI/pynxtools.git@workshop"

# your plugin in editable mode
uv pip install -e ".[dev]"
```

### Verify the setup

```bash
dataconverter --help
```

If you see the help text, you're ready.

---

## 1 — Know your data (~20 min)

Your example data lives in `tests/data/workshop-example/`.
Open the `README.md` there now — it describes every file.

### Explore the HDF5 file

Run this using Python:

```python
import h5py

with h5py.File("tests/data/workshop-example/mock_data.h5", "r") as f:
    def show(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(f"  {name:55s}  {obj[()]}")
    f.visititems(show)
```

You should see output like:

```
  data/x_units                                             b'eV'
  data/x_values                                            [-10. ... 10.]
  data/y_units                                             b'counts_per_second'
  data/y_values                                            [3.7e-06 ... 3.7e-06]
  metadata/instrument/detector/count_time                  1.2
  metadata/instrument/detector/count_time_units            b's'
  metadata/instrument/detector/name                        b'my_gaussian_detector'
  metadata/instrument/version                              1.0
```

!!! note "Why `b'eV'` instead of `'eV'`?"
    h5py returns string datasets as Python `bytes` objects.  The NeXus writer
    handles them correctly, so you don't need to convert them.  But if you
    ever need a plain string in Python, call `.decode()` — e.g. `b'eV'.decode()`.

Write down the paths to the datasets you will need:

- Signal data: `data/y_values`
- Energy axis: `data/x_values`
- Axis unit: `data/x_units`
- Signal unit: `data/y_units`
- Instrument version: `metadata/instrument/version`
- Detector count time: `metadata/instrument/detector/count_time`
- Count time unit: `metadata/instrument/detector/count_time_units`

### Read the ELN file

```bash
cat tests/data/workshop-example/eln_data.yaml
```

You will see:

```yaml
title: My experiment
user:
  name: John Doe
  address: 123 Science Rd, Data City, DC
sample:
  name: my_sample
  physical_form: powder
  temperature:
    value: 300
    unit: K
```

This is the metadata that does not come from the instrument — the user fills it
in manually.  Today it lives in a YAML file; in a real lab it could come from a
web form or an electronic lab notebook system.

---

## 2 — Understand the application definition (~15 min)

An application definition specifies what a valid NeXus file must contain.
Open `tests/data/workshop-example/NXsimple.nxdl.xml` and look at its structure.

You will see groups, fields, and attributes.  Each element has an **optionality**:

| Value | Meaning |
|---|---|
| *(nothing / default)* | **Required** — must be present |
| `recommended="true"` | **Recommended** — include if possible |
| `optional="true"` | **Optional** — may be omitted |

Now generate the **template** — the full list of paths the appdef expects:

```bash
dataconverter generate-template --nxdl NXsimple
```

The output shows every path and its requirement level.
Keep this open — you will use it when writing the config file.

!!! tip "Path notation"
    Paths look like `/ENTRY[entry]/USER[user]/name`.  The `USER` part is the
    NeXus class name; `[user]` is the instance name used in the HDF5 file.
    In the config file you write `/ENTRY/USER[user]/name` — the base class
    fills in `[entry]` automatically.

---

## 3 — Exercise 1: Read the HDF5 file (~25 min)

Open `src/pynxtools_simple/reader.py`.

You will see the `SimpleReader` class with several methods.
Each method has a `# TODO` comment explaining what to implement.
Read the entire file before writing any code.

### Your task

Implement `handle_hdf5_file` so that it reads the entire HDF5 file into
a flat Python dictionary stored in `self.hdf5_data`.

The dictionary should map slash-separated paths to values:

```python
{
    "data/x_values":   np.ndarray,        # shape (100,)
    "data/y_values":   np.ndarray,        # shape (100,)
    "data/x_units":    b"eV",
    "data/y_units":    b"counts_per_second",
    "metadata/instrument/version":  1.0,
    ...
}
```

**Steps:**

1. Add `import h5py` at the top of `reader.py`
2. Add `"h5py"` to the `dependencies` list in `pyproject.toml`
3. Reinstall your plugin: `uv pip install -e .`
4. Implement the method body (see the docstring in `reader.py` for hints)

### Check your work

Open a Python file in your project directory and run:

```python
from pynxtools_simple.reader import SimpleReader

r = SimpleReader()
r.handle_hdf5_file("tests/data/workshop-example/mock_data.h5")

print("Keys found:", list(r.hdf5_data.keys()))
print("x_values shape:", r.hdf5_data["data/x_values"].shape)
print("instrument version:", r.hdf5_data["metadata/instrument/version"])
```

Expected output:
```
Keys found: ['data/x_units', 'data/x_values', 'data/y_units', 'data/y_values',
             'metadata/instrument/detector/count_time', ...]
x_values shape: (100,)
instrument version: 1.0
```

??? success "Solution — reveal only after trying!"

    First, add `import h5py` at the top of `reader.py`.
    Then add `"h5py"` to `dependencies` in `pyproject.toml` and run
    `uv pip install -e .`.

    ```python
    def handle_hdf5_file(self, file_path: str) -> dict[str, Any]:
        def _recurse(group, path=""):
            result = {}
            for key, item in group.items():
                full = f"{path}/{key}" if path else key
                if isinstance(item, h5py.Group):
                    result.update(_recurse(item, full))
                elif isinstance(item, h5py.Dataset):
                    result[full] = item[()]
            return result

        with h5py.File(file_path, "r") as hdf:
            self.hdf5_data = _recurse(hdf)
        return {}
    ```

    **Why return `{}`?**
    The handler stores data on `self` for later use by the callbacks.
    The template is populated later by the config file — not directly by the handler.

---

## 4 — Exercise 2: Read the ELN file (~25 min)

### 4a — `CONVERT_DICT`

Near the top of `reader.py` you will find a dictionary called `CONVERT_DICT`.

When `parse_yml` flattens the YAML file into a Python dict, it uses this mapping
to rename path components.  Without it, the YAML key `user/name` would become
the path `/ENTRY[entry]/user/name` — but NeXus requires the group to be called
`USER[user]`, giving `/ENTRY[entry]/USER[user]/name`.

**Your task:** add four entries to `CONVERT_DICT`:

| YAML key | NeXus group notation |
|---|---|
| `"user"` | `"USER[user]"` |
| `"instrument"` | `"INSTRUMENT[instrument]"` |
| `"detector"` | `"DETECTOR[detector]"` |
| `"sample"` | `"SAMPLE[sample]"` |

The entries for `"unit"` and `"version"` are already there as examples.

??? success "Solution"

    ```python
    CONVERT_DICT: dict[str, str] = {
        "unit": "@units",
        "version": "@version",
        "user": "USER[user]",
        "instrument": "INSTRUMENT[instrument]",
        "detector": "DETECTOR[detector]",
        "sample": "SAMPLE[sample]",
    }
    ```

### 4b — `handle_eln_file`

**Your task:** implement `handle_eln_file`.

Use the `parse_yml` utility from pynxtools:

```python
from pynxtools.dataconverter.readers.utils import parse_yml
```

Call it with:
- `file_path` — the YAML file path
- `convert_dict=CONVERT_DICT` — apply the key mapping
- `parent_key="/ENTRY[entry]"` — prefix every key with this string

Store the result in `self.eln_data` and return `{}`.

### Check your work

```python
from pynxtools_simple.reader import SimpleReader

r = SimpleReader()
r.handle_eln_file("tests/data/workshop-example/eln_data.yaml")

for key, value in r.eln_data.items():
    print(f"  {key}  =  {value}")
```

Expected output:
```
  /ENTRY[entry]/title  =  My experiment
  /ENTRY[entry]/USER[user]/name  =  John Doe
  /ENTRY[entry]/USER[user]/address  =  123 Science Rd, Data City, DC
  /ENTRY[entry]/SAMPLE[sample]/name  =  my_sample
  /ENTRY[entry]/SAMPLE[sample]/physical_form  =  powder
  /ENTRY[entry]/SAMPLE[sample]/temperature  =  300
  /ENTRY[entry]/SAMPLE[sample]/temperature/@units  =  K
```

!!! tip "Why does `temperature` appear as `300` and `@units` as `K`?"
    In the YAML, temperature is written as:
    ```yaml
    temperature:
      value: 300
      unit: K
    ```
    The `CONVERT_DICT` entry `"unit": "@units"` renames the `unit` key to `@units`,
    and `parse_yml` unwraps the `value:` key automatically.

??? success "Solution"

    Add this import at the top of `reader.py`:
    ```python
    from pynxtools.dataconverter.readers.utils import parse_yml
    ```

    Then implement the method:
    ```python
    def handle_eln_file(self, file_path: str) -> dict[str, Any]:
        self.eln_data = parse_yml(
            file_path,
            convert_dict=CONVERT_DICT,
            parent_key="/ENTRY[entry]",
        )
        return {}
    ```

---

## 5 — Exercises 3–5: Callback methods (~30 min)

Now that your data is loaded, you need to expose it to the config file via
**callbacks**.  Each `@`-prefix in the config file calls one of these methods.

### How callbacks work

When the `MultiFormatReader` processes the config file, it reads each value.
If the value starts with `@`, it calls the corresponding method:

| Config value | Method called | Arguments |
|---|---|---|
| `"@attrs:metadata/instrument/version"` | `get_attr` | `key="/ENTRY[entry]/..."`, `path="metadata/instrument/version"` |
| `"@eln"` | `get_eln_data` | `key="/ENTRY[entry]/USER[user]/name"`, `path=""` |
| `"@data:x_values"` | `get_data` | `key="/ENTRY[entry]/data/x_values"`, `path="x_values"` |

The `key` is always the full NeXus template path being populated.
The `path` is what comes after the colon in the `@prefix:path` notation.

### Exercise 3: `get_attr`

Implement `get_attr` to return instrument metadata from `self.hdf5_data`.

Use `path` to look up the value — it matches the keys in `self.hdf5_data`.

??? success "Solution"

    ```python
    def get_attr(self, key: str, path: str) -> Any:
        if self.hdf5_data is None:
            return None
        return self.hdf5_data.get(path)
    ```

### Exercise 4: `get_eln_data`

Implement `get_eln_data` to return ELN metadata from `self.eln_data`.

!!! info "Use `key`, not `path`"
    For ELN data, `parse_yml` already produced dictionary keys that match
    the full NeXus template paths (e.g. `/ENTRY[entry]/USER[user]/name`).
    The `key` argument is exactly that path, so use `key` — not `path` — for
    the lookup.  The `path` argument is empty for plain `"@eln"` entries.

??? success "Solution"

    ```python
    def get_eln_data(self, key: str, path: str) -> Any:
        if self.eln_data is None:
            return None
        return self.eln_data.get(key)
    ```

### Exercise 5: `get_data`

Implement `get_data` to return measurement arrays from `self.hdf5_data`.

The arrays live under `"data/x_values"` and `"data/y_values"` in
`self.hdf5_data`.  The `path` argument will be `"x_values"` or `"y_values"`,
so look up `f"data/{path}"`.

??? success "Solution"

    ```python
    def get_data(self, key: str, path: str) -> Any:
        if self.hdf5_data is None:
            return None
        data = self.hdf5_data.get(f"data/{path}")
        if data is None:
            logger.warning(f"No data found at 'data/{path}'.")
        return data
    ```

### ✅ Checkpoint — test all callbacks

```python
from pynxtools_simple.reader import SimpleReader

r = SimpleReader()
r.handle_hdf5_file("tests/data/workshop-example/mock_data.h5")
r.handle_eln_file("tests/data/workshop-example/eln_data.yaml")

# Test get_attr
print(r.get_attr("", "metadata/instrument/version"))        # → 1.0
print(r.get_attr("", "metadata/instrument/detector/count_time"))  # → 1.2

# Test get_eln_data
print(r.get_eln_data("/ENTRY[entry]/USER[user]/name", ""))  # → John Doe
print(r.get_eln_data("/ENTRY[entry]/title", ""))            # → My experiment

# Test get_data
print(r.get_data("", "x_values").shape)  # → (100,)
print(r.get_data("", "y_values").shape)  # → (100,)
```

---

## 6 — Exercise 6: Write the config file (~35 min)

The config file is the **semantic bridge** between your data and the NeXus
application definition.

It is a JSON file where:
- **Keys** are NeXus template paths (from `generate-template`)
- **Values** tell the reader where to find the data using `@`-prefixes

### Step 1 — compare the appdef to your data

Run `dataconverter generate-template --nxdl NXsimple` again.
For each required or recommended path, decide:

- Is the value in `self.hdf5_data`? → use `"@attrs:<hdf5-path>"`
- Is the value in `self.eln_data`? → use `"@eln"`
- Is it a measurement array? → use `"@data:<array-name>"`
- Is it a fixed value? → write the value directly (string, number, list)

### Step 2 — path notation in the config

Use `/ENTRY/` (without `[entry]`) in config keys — the base class replaces it with `/ENTRY[entry]/` for each entry name automatically.

For nested group keys, you can write them either flat or nested:

```json
// flat
{ "/ENTRY/USER[user]/name": "@eln" }

// nested (equivalent, easier to read)
{ "/ENTRY/USER[user]": { "name": "@eln" } }
```

### Step 3 — fill in the table

| NeXus path | Source | Config value |
|---|---|---|
| `/ENTRY/title` | ELN | `"@eln"` |
| `/ENTRY/USER[user]/name` | ELN | `"@eln"` |
| `/ENTRY/USER[user]/address` | ELN | `"@eln"` |
| `/ENTRY/INSTRUMENT[instrument]/@version` | HDF5 `metadata/instrument/version` | `"@attrs:metadata/instrument/version"` |
| `/ENTRY/INSTRUMENT[instrument]/DETECTOR[detector]/count_time` | HDF5 | `"@attrs:metadata/instrument/detector/count_time"` |
| `/ENTRY/INSTRUMENT[instrument]/DETECTOR[detector]/count_time/@units` | HDF5 | `"@attrs:metadata/instrument/detector/count_time_units"` |
| `/ENTRY/SAMPLE[sample]/name` | ELN | `"@eln"` |
| `/ENTRY/SAMPLE[sample]/physical_form` | ELN | `"@eln"` |
| `/ENTRY/SAMPLE[sample]/temperature` | ELN | `"@eln"` |
| `/ENTRY/SAMPLE[sample]/temperature/@units` | ELN | `"@eln"` |
| `/ENTRY/data/@axes` | fixed | `["x_values"]` |
| `/ENTRY/data/@signal` | fixed | `"data"` |
| `/ENTRY/data/data` | HDF5 `data/y_values` | `"@data:y_values"` |
| `/ENTRY/data/x_values` | HDF5 `data/x_values` | `"@data:x_values"` |

Create `tests/data/workshop-example/my_config.json` and fill it in.

??? success "Solution"

    ```json title="my_config.json"
    {
      "/ENTRY/title": "@eln",
      "/ENTRY/USER[user]": {
        "name": "@eln",
        "address": "@eln"
      },
      "/ENTRY/INSTRUMENT[instrument]": {
        "@version": "@attrs:metadata/instrument/version",
        "DETECTOR[detector]": {
          "count_time": "@attrs:metadata/instrument/detector/count_time",
          "count_time/@units": "@attrs:metadata/instrument/detector/count_time_units"
        }
      },
      "/ENTRY/SAMPLE[sample]": {
        "name": "@eln",
        "physical_form": "@eln",
        "temperature": "@eln",
        "temperature/@units": "@eln"
      },
      "/ENTRY/data": {
        "@axes": ["x_values"],
        "@signal": "data",
        "data": "@data:y_values",
        "x_values": "@data:x_values"
      }
    }
    ```

---

## 7 — Run the converter (~15 min)

```bash
dataconverter \
    tests/data/workshop-example/mock_data.h5 \
    tests/data/workshop-example/eln_data.yaml \
    tests/data/workshop-example/my_config.json \
    --reader simple \
    --nxdl NXsimple \
    --output output.nxs
```

If the conversion succeeds, `output.nxs` appears in your working directory.
If required fields are missing, the converter will tell you which ones — go
back to your config file and add them.

### Inspect the output

```python
import h5py

with h5py.File("output.nxs", "r") as f:
    def show(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(f"  {name}")
    f.visititems(show)
```

Compare the paths in `output.nxs` against the `generate-template` output —
every required path should be present.

---

## 8 — Run the tests (~15 min)

The template already includes a test framework.  For the workshop, a reference
output file is provided in `tests/data/workshop-example/`.

Generate it from your working reader:

```bash
dataconverter \
    tests/data/workshop-example/mock_data.h5 \
    tests/data/workshop-example/eln_data.yaml \
    tests/data/workshop-example/config_file.json \
    --reader simple \
    --nxdl NXsimple \
    --output tests/data/workshop-example/output_reference.nxs
```

Then update `tests/test_reader.py` to point at the example data folder:

```python
test_cases = [
    ("workshop-example", [], {}, "workshop-example"),
]
```

And run:

```bash
pytest tests/test_reader.py -v
```

For more on the test framework, see
[How-to: Test your reader](../how-tos/pynxtools/using-pynxtools-test-framework.md).

---

## Troubleshooting

| Symptom | Most likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: h5py` | h5py not installed | Add `"h5py"` to `dependencies` in `pyproject.toml`, run `uv pip install -e .` |
| `NXsimple not found` | Wrong pynxtools version | Run `pip install "pynxtools @ git+https://…@workshop"` |
| `Required field /ENTRY/.../X missing` | Config doesn't map that path | Add the missing key to your config file |
| Callback always returns `None` | Handler didn't run | Check that the file extension is in `self.extensions`; print `self.hdf5_data` |
| `get_eln_data` always returns `None` | Wrong lookup key | Print `key` and `list(self.eln_data.keys())` side by side |
| Byte string in output | h5py returns bytes | Usually fine — NeXus handles it. Decode with `.decode()` if needed in Python |
| Template path mismatch | Typo in config key | Copy-paste from `generate-template` output |

---

## Bonus exercises (if you finish early)

### Bonus A — add a `post_process` step

Add a `post_process` method to your reader that computes the peak position of the
Gaussian signal and stores it in the template:

```python
def post_process(self) -> None:
    """Compute peak position from y_values and store it."""
    import numpy as np
    if self.hdf5_data is None:
        return
    x = self.hdf5_data.get("data/x_values")
    y = self.hdf5_data.get("data/y_values")
    if x is not None and y is not None:
        peak_idx = np.argmax(y)
        # store directly in the template dict via self.config_dict
        # or inject via get_attr by adding to hdf5_data:
        self.hdf5_data["derived/peak_position"] = x[peak_idx]
        self.hdf5_data["derived/peak_position_units"] = b"eV"
```

### Bonus B — handle a second file format

What if users also provide a plain CSV file with additional calibration data?

Add `.csv` to `self.extensions`:

```python
self.extensions[".csv"] = self.handle_csv_file
```

Implement `handle_csv_file` using the `csv` or `pandas` module.
Store the data in `self.csv_data` and expose it via `get_attr`.

### Bonus C — explore the output with h5py

Write a script that reads `output.nxs` and plots the signal using `matplotlib`:

```python
import h5py
import matplotlib.pyplot as plt

with h5py.File("output.nxs", "r") as f:
    x = f["entry/data/x_values"][()]
    y = f["entry/data/data"][()]

plt.plot(x, y)
plt.xlabel("Energy (eV)")
plt.ylabel("Counts per second")
plt.title("Gaussian detector signal")
plt.show()
```

---

## Summary

| Step | What you did | Key concept |
|---|---|---|
| Setup | Created a plugin from the template | Entry point registration in `pyproject.toml` |
| Exercise 1 | `handle_hdf5_file` | Flat dict mapping from HDF5 paths to values |
| Exercise 2a | `CONVERT_DICT` | Renaming YAML groups to NeXus class notation |
| Exercise 2b | `handle_eln_file` | `parse_yml` for ELN → template paths |
| Exercises 3–5 | Three callback methods | The `@prefix:path` dispatch pattern |
| Exercise 6 | `config_file.json` | Semantic source↔NeXus mapping |
| Run | `dataconverter` | Validation is automatic |
| Tests | `pytest` | Reproducibility testing |
| Section 7 | Uploaded to NOMAD | NeXus files are parsed automatically; explore via DATA tab and NORTH |

---

## 7 — Upload your NeXus file to NOMAD

You have produced a validated `.nxs` file. This section shows how to bring it
into [NOMAD](https://nomad-lab.eu) — the research data management platform that
understands NeXus natively — so that your data becomes findable, searchable, and
shareable.

### 7.1 Where to go

| Instance | URL | Who it is for |
|---|---|---|
| NOMAD production | nomad-lab.eu/prod/v1/gui | Public datasets |
| NOMAD test | nomad-lab.eu/prod/v1/test/gui | Safe to experiment — data is not permanent |
| Local deployment | `localhost:8080` | Your own NOMAD install |

You need a free NOMAD account to upload. Create one via **Login → Register** on
any of the instances above. Browsing published data is always public.

<!-- IMAGE: NOMAD landing page showing the Login button and search bar -->

### 7.2 Create an upload and drop your file

1. Log in and go to **Publish → Your uploads**.
2. Click **CREATE NEW UPLOAD** and give it a name (e.g. "double-slit workshop").
3. Drag and drop `output.nxs` onto the upload area, or click to browse for it.
4. NOMAD detects the `.nxs` extension, identifies the parser, and starts
   processing automatically.
5. Wait for the green **processed** indicator next to the entry.

<!-- IMAGE: Upload overview page with the drag-drop area highlighted -->

!!! tip
    You can upload a `.zip` file containing `output.nxs` plus any auxiliary
    files (ELN YAML, raw data). NOMAD extracts the archive and processes each
    file independently.

### 7.3 Explore your entry

Click the arrow icon → next to the entry to open the entry page. Three tabs are
available:

| Tab | What you see |
|---|---|
| **OVERVIEW** | Summary cards: metadata on the left, visualizations on the right |
| **FILES** | The raw `.nxs` file and any auxiliary files in the upload |
| **DATA** | The fully parsed NeXus tree — every group and field from your NXDL |

The **DATA** tab is the most interesting for NeXus work: it renders the
HDF5 hierarchy using NOMAD's metainfo schema, with unit-aware values and
inline documentation drawn from the NXDL `<doc>` strings.

<!-- IMAGE: Entry DATA tab showing the NXentry → NXinstrument → NXdetector hierarchy -->

### 7.4 View in the NeXus app and filter by definition

**Search and filter:**

1. Go to **Explore → Entries** in the top menu.
2. Open the filter panel on the left.
3. Under **Data**, expand the **NeXus** filter group.
4. Set **Application definition** to `NXsimple` (or whichever definition your
   file uses) to show only matching entries.

**NeXus viewer:**

On the entry **OVERVIEW** page, look for the *NeXus* card. It opens an
interactive tree viewer that mirrors the HDF5 structure and lets you browse
groups, fields, and attributes without downloading the file.

<!-- IMAGE: Explore → Entries page with the NeXus filter expanded, showing "NXsimple" selected -->

### 7.5 Analyze with NORTH

NORTH (NOMAD Remote Tools Hub) runs containerized Jupyter notebooks that connect
directly to the files in your upload — no download needed.

1. From the entry **OVERVIEW** page, click **Analyze in NORTH** (or navigate to
   **Analyze → NORTH tools** from the top menu).
2. Choose a container. The generic **Jupyter** tool works for standard Python
   analysis.
3. NOMAD launches the container and mounts your upload directory. A new Jupyter
   tab opens in the browser.
4. Inside the notebook, the upload path is available via an environment variable:

    ```python
    import h5py, os

    upload_path = os.environ.get("NOMAD_UPLOAD_PATH", ".")
    with h5py.File(f"{upload_path}/output.nxs", "r") as f:
        data = f["entry/data/data"][()]
        print(data.shape)
    ```

5. Any files you write back into the upload directory are stored in NOMAD. Click
   **Reprocess** on the upload page to re-index newly created entries.

<!-- IMAGE: NORTH Jupyter notebook open in a browser tab with a plot of the interference pattern -->

!!! note
    NORTH availability depends on the NOMAD deployment. The public instance at
    nomad-lab.eu has NORTH enabled. Local deployments need a separate NORTH
    configuration — see
    [NOMAD docs > NORTH](https://nomad-lab.eu/prod/v1/docs/explanation/north.html).

---

**Well done!**
Tomorrow you will apply the same pattern to your own data and your own
application definition.  See [Day 2 — Bring Your Own Data](bring-your-own-data.md).
