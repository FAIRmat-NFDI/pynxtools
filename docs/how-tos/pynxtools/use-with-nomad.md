# Use pynxtools with NOMAD

This how-to covers practical workflows for using `pynxtools` together with NOMAD, such as
uploading NeXus files via the API, verifying that your file is parsed correctly, and
configuring a NOMAD OASIS instance.

For the conceptual background see
[Learn → pynxtools → pynxtools and NOMAD](../../learn/pynxtools/nomad-integration.md).

For a graphical-interface upload walkthrough see the
[Tutorial → Uploading NeXus data to NOMAD](../../tutorial/nexus-to-nomad.md).

---

## Prerequisites

- A valid NeXus file — see [How-tos → Validate NeXus files](validate-nexus-files.md) to check your file before uploading
- A NOMAD account (public instance) or a running NOMAD OASIS

---

## Upload via the NOMAD Python API

The `nomad-lab` package provides a Python client for the NOMAD REST API.

### Install the client

```bash
pip install nomad-lab
```

### Authenticate

```python
from nomad.client import Auth

auth = Auth(username="your_username", password="your_password")
# For the public instance:
# auth = Auth(user="you@example.com", password="…", url="https://nomad-lab.eu/prod/v1/api/v1")
```

Alternatively, use an API token from your NOMAD account settings
(`Your account → API tokens`) to avoid storing credentials:

```python
from nomad.client import Auth
auth = Auth(access_token="your_api_token")
```

### Create an upload and add a file

```python
from nomad.client import upload_file

# Create a new upload and add the NeXus file
upload_id = upload_file(
    file_path="my_data.nxs",
    auth=auth,
)
print(f"Upload created: {upload_id}")
```

### Check processing status

```python
import requests

url = f"https://nomad-lab.eu/prod/v1/api/v1/uploads/{upload_id}"
resp = requests.get(url, headers=auth.headers())
print(resp.json()["data"]["process_status"])
# "SUCCESS" means pynxtools parsed the file successfully
```

### Publish the upload

```python
resp = requests.post(
    f"https://nomad-lab.eu/prod/v1/api/v1/uploads/{upload_id}/action/publish",
    headers=auth.headers(),
)
print(resp.json()["data"]["publish_time"])
```

For the full API reference see the
[NOMAD API documentation](https://nomad-lab.eu/prod/v1/api/v1/extensions/docs).

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
from nomad.datamodel import EntryArchive
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

2. **Check the `definition` field** — NOMAD relies on `/entry/definition` to select the correct schema. Verify it is set and matches a known application definition:
   ```bash
   read_nexus my_data.nxs -d /entry/definition
   ```

3. **Check which parser was selected** — in the NOMAD GUI, go to your entry and open the **LOG** tab. The log shows which parser was invoked and if any warnings or errors were raised.

4. **Test the NOMAD parser locally** (see the code snippet above) and check for Python exceptions or missing Metainfo fields.

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
### Test the OASIS parser

After restarting the OASIS workers, upload a known-good NeXus file to verify the
parser runs correctly. Use the OASIS GUI or the API at your OASIS endpoint:

```python
from nomad.client import Auth
auth = Auth(
    access_token="your_oasis_token",
    url="https://your-oasis.example.com/nomad/api/v1",
)
```

---

## Upload a batch of files

```python
import os
from pathlib import Path
from nomad.client import upload_file, Auth

auth = Auth(access_token="your_api_token")
data_dir = Path("./nexus_data")

for nxs_file in data_dir.glob("*.nxs"):
    upload_id = upload_file(str(nxs_file), auth=auth)
    print(f"{nxs_file.name} → upload {upload_id}")
```

Each `.nxs` file creates a separate NOMAD upload. If you want all files grouped under one DOI, you can add them to the same upload by using the upload API directly:

```python
import requests

# Create one upload
resp = requests.post(
    "https://nomad-lab.eu/prod/v1/api/v1/uploads",
    headers=auth.headers(),
    json={"upload_name": "my_batch"},
)
upload_id = resp.json()["upload_id"]

# Add files one by one
for nxs_file in data_dir.glob("*.nxs"):
    with open(nxs_file, "rb") as f:
        requests.put(
            f"https://nomad-lab.eu/prod/v1/api/v1/uploads/{upload_id}/raw/{nxs_file.name}",
            headers=auth.headers(),
            data=f,
        )
```

---

## Next steps

- [Learn → pynxtools and NOMAD](../../learn/pynxtools/nomad-integration.md) — how the parser pipeline works
- [NOMAD API documentation](https://nomad-lab.eu/prod/v1/api/v1/extensions/docs)
- [NOMAD OASIS installation guide](https://nomad-lab.eu/prod/v1/docs/howto/oasis/install.html)
