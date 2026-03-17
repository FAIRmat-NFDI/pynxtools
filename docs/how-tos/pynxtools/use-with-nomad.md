# Use pynxtools with NOMAD

This how-to covers practical workflows for using `pynxtools` together with NOMAD, such as uploading NeXus files via the API, verifying that your file is parsed correctly, and configuring API calls for a NOMAD OASIS instance.

For the conceptual background see
[Learn → pynxtools → pynxtools and NOMAD](../../learn/pynxtools/nomad-integration.md).

For a graphical-interface upload walkthrough see the
[Tutorial → Uploading NeXus data to NOMAD](../../tutorial/nexus-to-nomad.md).

---

## Prerequisites

- A valid NeXus file — see [How-tos → Validate NeXus files](validate-nexus-files.md) to check your file before uploading
- A NOMAD account (test instance) or a running NOMAD OASIS

---

## Upload via the NOMAD Python API

NOMAD provides a REST API interface for programmatically working with NOMAD data.

For this how-to guide, we'll work with the [`nomad-utility-workflows`](https://github.com/FAIRmat-NFDI/nomad-utility-workflows)
package, which is a recommended wrapper package to interact with the NOMAD API from Python.


### Install

```bash
pip install nomad-utility-workflows
```

### Configure credentials

Create a `.env` file in your working directory (never commit this file):

```
NOMAD_USERNAME="your_username"
NOMAD_PASSWORD="your_password"
```

Credentials are loaded automatically via `python-decouple`; you do not need to pass them explicitly to any function.

### Choose the NOMAD deployment of interest

All API functions in `nomad-utility-workflows` allow the user to specify the NOMAD URL with the optional keyword argument `url`. You can learn about the natively-supported URLs in the `nomad-utility-workflows` documentation, see [nomad-utility-workflows -> How-tos > How to perform NOMAD API Calls](https://fairmat-nfdi.github.io/nomad-utility-workflows/how_to/use_api_functions.html#nomad-urls).

For this how-to guide, we'll work with the [NOMAD test deployment](https://nomad-lab.eu/prod/v1/test/). Set the URL accordingly:

```python
URL_TEST="test"
```

### Upload a file

NOMAD expects files to be uploaded as a **zip archive**. Pack your NeXus file first:

```python
import zipfile
from pathlib import Path

nxs_path = Path("my_data.nxs")
zip_path = Path("my_data.zip")

with zipfile.ZipFile(zip_path, "w") as zf:
    zf.write(nxs_path, arcname=nxs_path.name)
```

Then upload — pass `URL_TEST` to target the test NOMAD instance:

```python
from nomad_utility_workflows.utils.uploads import upload_files_to_nomad

upload_id = upload_files_to_nomad(filename=str(zip_path), url=URL_TEST)
print(f"Upload created: {upload_id}")
```

### Check processing status

```python
import time
from nomad_utility_workflows.utils.uploads import get_upload_by_id

while True:
    upload = get_upload_by_id(upload_id, url=URL_TEST)
    print(upload.process_status)
    if not upload.process_running:
        break
    time.sleep(10)

# process_status == "SUCCESS" means pynxtools parsed the file successfully
```

### Edit upload metadata

```python
from nomad_utility_workflows.utils.uploads import edit_upload_metadata

edit_upload_metadata(
    upload_id,
    url=URL_TEST,
    upload_metadata={
        "upload_name": "My NeXus dataset",
        "references": ["https://doi.org/xx.xxxx/xxxxxx"],
        "comment": "Uploaded via nomad-utility-workflows",
    },
)
```

### Publish the upload

In case you already want to publish your upload, run:

```python
from nomad_utility_workflows.utils.uploads import publish_upload

publish_upload(upload_id, url=URL_TEST)
```

You can now see your published upload in the [`Uploads` tab of the test deployment](https://nomad-lab.eu/prod/v1/test/gui/user/uploads).

---

## Verify that NOMAD can parse your file

Before uploading, run the `pynxtools` NOMAD parser locally to see what NOMAD will extract:

```bash
pip install nomad-lab pynxtools
```

```python
from nomad.datamodel import EntryArchive
from pynxtools.nomad.parser import NexusParser

archive = EntryArchive()
parser = NexusParser()
parser.parse("my_data.nxs", archive, logger=None)

# Inspect what was parsed
import json
print(json.dumps(archive.m_to_dict(), indent=2, default=str))
```

The output shows the Metainfo archive that NOMAD would index. Check that:

- Required fields from your application definition appear under `data`
- The technique name and instrument names are present
- Default plottable data is resolved (will appear under `results.properties`)

---

## Debug a failed upload

If NOMAD reports a parsing error or your entry shows no data:

1. **Validate the file locally first:**
   ```bash
   validate_nexus my_data.nxs
   ```
   Fix any errors or missing required fields before re-uploading.

2. **Check the `definition` field** — NOMAD relies on `/entry/definition` (or the definition field in other `NXentry` groups (e.g. `entry1`, `entry2`)) to select the correct schema. Verify it is set and matches a known application definition.

<!-- ```bash
read_nexus my_data.nxs -d /entry/definition
``` -->

3. **Check which parser was selected** — in the NOMAD GUI, go to your entry and open the **LOG** tab. The log shows which parser was invoked and if any warnings or errors were raised.

4. **Test the NOMAD parser locally** (see the code snippet above) and check for Python exceptions or missing Metainfo fields.

5. **Inspect entries after upload:**
   ```python
   from nomad_utility_workflows.utils.entries import get_entries_of_upload

   entries = get_entries_of_upload(upload_id, url=URL_TEST, with_authentication=True)
   for entry in entries:
       print(entry.entry_name, entry.processing_errors)
   ```

---

## Use pynxtools in a NOMAD OASIS

### Install pynxtools in the OASIS environment

Add `pynxtools` to the `pyproject.toml` of your OASIS
deployment. If you use reader plugins for specific techniques, add those too:

```toml
[project.optional-dependencies]
plugins = [
 "pynxtools",
 "pynxtools-em>=0.4",
 "pynxtools-xps>=0.5.3"
]
```

### Upload to an OASIS

Pass the full OASIS API URL instead of `URL_TEST`:

```python
upload_id = upload_files_to_nomad(
    filename="my_data.zip",
    url="https://your-oasis.example.com/nomad/api/v1",
)
```

All other functions (`get_upload_by_id`, `publish_upload`, `edit_upload_metadata`, …) accept the same `url` parameter.

---

## Upload a batch of files

Pack all files into a single zip archive to group them under one upload (and one DOI):

```python
import zipfile
from pathlib import Path
from nomad_utility_workflows.utils.uploads import (
    upload_files_to_nomad, edit_upload_metadata, publish_upload,
)

data_dir = Path("./nexus_data")
zip_path = Path("batch.zip")

with zipfile.ZipFile(zip_path, "w") as zf:
    for nxs_file in data_dir.glob("*.nxs"):
        zf.write(nxs_file, arcname=nxs_file.name)

upload_id = upload_files_to_nomad(filename=str(zip_path), url=URL_TEST)
print(f"Batch upload: {upload_id}")
```

If you need separate uploads per file, call `upload_files_to_nomad` once per zip:

```python
for nxs_file in data_dir.glob("*.nxs"):
    single_zip = nxs_file.with_suffix(".zip")
    with zipfile.ZipFile(single_zip, "w") as zf:
        zf.write(nxs_file, arcname=nxs_file.name)
    uid = upload_files_to_nomad(filename=str(single_zip), url=URL_TEST)
    print(f"{nxs_file.name} → upload {uid}")
```

---

## Next steps

- [Learn → pynxtools and NOMAD](../../learn/pynxtools/nomad-integration.md) — how the parser pipeline works
- [`nomad-utility-workflows` documentation](https://fairmat-nfdi.github.io/nomad-utility-workflows)
- [NOMAD API documentation](https://nomad-lab.eu/prod/v1/api/v1/extensions/docs)
- [NOMAD OASIS installation guide](https://nomad-lab.eu/prod/v1/docs/howto/oasis/install.html)
