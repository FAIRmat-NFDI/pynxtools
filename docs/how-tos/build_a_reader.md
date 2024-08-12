# How to build your own reader

Your current data is not supported yet by the [built-in pynxtools readers](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/src/pynxtools/dataconverter/readers) or any of the officially supported [pynxtools plugins](..\reference\plugins.md)? 

Don't worry, the following how-to will guide you how to write a reader your own data.

## Getting started
You should start by creating a clean repository that implements the following structure (for a plugin called ```pynxtools-plugin```):
```
pynxtools-plugin
├── .github/workflows
├── docs
│   ├── explanation
│   ├── how-tos
│   ├── reference
│   ├── tutorial
├── src
│   ├── pynxtools_plugin
│       ├── reader.py
├── _layouts
│   ├── default.html
│   └── post.html
├── tests
│   └── data
├── LICENSE
├── mkdocs.yaml
├── dev-requirements.txt
└── pyproject.toml
```

To identify `pynxtools-plugin` as a plugin for pynxtools, an entry point must be established:
```
[project.entry-points."pynxtools.reader"]
myreader = "pynxtools_plugin.reader:MyDataReader"
```

Note: There is also a [cookiecutter template](https://github.com/FAIRmat-NFDI/pynxtools-plugin-template) available for creating your own pynxtools plugin, but this is currently not well-maintained.


## Writing a Reader

The pynxtools converter allows extending support to other data formats by allowing extensions called readers.
The converter provides a dev platform to build a NeXus compatible reader by providing checking against a chosen NeXus Application Definition.

After you have established the main structure, you can start writing your reader. The new reader shall be placed in `reader.py`.

Then implement the reader function:

```python
"""MyDataReader implementation for the DataConverter to convert mydata to NeXus."""
from typing import Tuple, Any

from pynxtools.dataconverter.readers.base.reader import BaseReader

class MyDataReader(BaseReader):
    """MyDataReader implementation for the DataConverter to convert mydata to NeXus."""

    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        objects: Tuple[Any] = None
    ) -> dict:
        """Reads data from given file and returns a filled template dictionary"""
        # Fill the template
        for path in file_paths:
            print(path)

        template["/entry/instrument/scan"] = raw_scan_data

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = MyDataReader

```

The read function takes a template dictionary based on the provided NXDL file (similar to `dataconverter generate-template`) and the list of all the file paths the user provides.
The returned dictionary should contain keys that exist in the template as defined below.
The values of these keys have to be data objects to be populated in the output NeXus file.
They can be lists, numpy arrays, numpy bytes, numpy floats, numpy ints. Practically you can pass any value that can be handled by the `h5py` package.

The dataconverter can be executed using:

```console
user@box:~$ dataconverter --reader mydatareader --nxdl NXmynxdl --output path_to_output.nxs
```

### The reader template dictionary

Example:

```json
{
  "/entry/instrument/source/type": "None"
}
```

**Units**: If there is a field defined in the NXDL, the converter expects a filled in /data/@units entry in the template dictionary corresponding to the right /data field unless it is specified as NX_UNITLESS in the NXDL. Otherwise, you will get an exception.

```json
{
  "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/data": "None",
  "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/data/@units": "Should be set to a string value"
}
```

In case the NXDL does not define a `name` for the group the requested data belongs to, the template dictionary will list it as `/NAME_IN_NXDL[name_in_output_nexus]`
You can choose any name you prefer instead of the suggested name. This allows the reader function to repeat groups defined in the NXDL to be outputted to the NeXus file.

```json
{
  "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/type": "None"
}
```

For attributes defined in the NXDL, the reader template dictionary will have the assosciated key with a "@" prefix to the attributes name at the end of the path:

```json
{
  "/entry/instrument/source/@attribute": "None"
}
```

You can also define links by setting the value to sub dictionary object with key `link`:

```python
template["/entry/instrument/source"] = {"link": "/path/to/source/data"}
```

For a given NXDL schema, you can generate an empty template with the command
```console
user@box:~$ dataconverter generate-template` --nxdl NXmynxdl
```

<img src="./convert_routine.svg" />



## How to use the built-in MultiFormatReader

While building on the ```BaseReader``` allows for the most flexibility, in most cases it is desirable to implement a reader that can read in multiple file formats and then populate the template based on the read data. For this purpose, `pynxtools` has the [**`MultiFormatReader`**](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/multi/reader.py#L310), which can be readily extended for your own data.

In case you want to make use of the `MultiFormatReader`, the following basic structure must be implemented.
```python
"""MyDataReader implementation for the DataConverter to convert mydata to NeXus."""
from typing import Tuple, Any

from pynxtools.dataconverter.readers.base.reader import ParseJsonCallbacks, MultiFormatReader

class MyDataReader(MultiFormatReader):
    """MyDataReader implementation for the DataConverter to convert mydata to NeXus."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.extensions = {
            ".yml": self.handle_eln_file,
            ".yaml": self.handle_eln_file,
            ".json": self.set_config_file,
            # Here you must add functions for handling any other file extension
        }
# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = MyDataReader
```

In order to understand the capabilities of the `MultiFormatReader` and which method you need to implement when extending it, we will have a look at its ```read``` method:
```
def read(
    self,
    template: dict = None,
    file_paths: Tuple[str] = None,
    objects: Optional[Tuple[Any]] = None,
    **kwargs,
) -> dict:
    self.kwargs = kwargs
    self.config_file = self.kwargs.get("config_file", self.config_file)
    self.overwrite_keys = self.kwargs.get("overwrite_keys", self.overwrite_keys)   
```
### Template initialization and processing order
An empty `Template` object is initialized that later gets filled from the data files later.
```
    template = Template(overwrite_keys=self.overwrite_keys)

    def get_processing_order(path: str) -> Tuple[int, Union[str, int]]:
        """
        Returns the processing order of the file.
        """
        ext = os.path.splitext(path)[1]
        if self.processing_order is None or ext not in self.processing_order:
            return (1, ext)
        return (0, self.processing_order.index(ext))

    sorted_paths = sorted(file_paths, key=get_processing_order)
```
If the reader has a `self.processing_order`, the input files get sorted in this order. If `self.overwrite_keys` is True, later files get precedent.
### Reading of input files
```
    for file_path in sorted_paths:
        extension = os.path.splitext(file_path)[1].lower()
        if extension not in self.extensions:
            logger.warning(
                f"File {file_path} has an unsupported extension, ignoring file."
            )
            continue
        if not os.path.exists(file_path):
            logger.warning(f"File {file_path} does not exist, ignoring entry.")
            continue

        template.update(self.extensions.get(extension, lambda _: {})(file_path))
```
This parts reads in the data from all data files. The `MultiFormatReader` has an `extensions` property, which is a dictionary that for each file extension calls a function that reads in data from files with that extension. If you have e.g. an HDF5 file, you would have to add a method for handling this type of file, i.e., `self.extensions[".hdf5"] = self.handle_hdf5`. Note that any of these methods take as input only the file path, e.g.
```
def handle_eln_file(self, file_path: str) -> Dict[str, Any]
```

Note that for several input formats, standardized readers already exist within the `MultiFormatReader`. For example, YAML files can be parsed using the `pynxtools.dataconverter.readers.utils.parse_yml` function.

### Setting default values in the template
```
    template.update(self.setup_template())
```
### Handling objects
```
    if objects is not None:
        template.update(self.handle_objects(objects))
```
### Parsing the config file
```
    if self.config_file is not None:
        self.config_dict = parse_flatten_json(
            self.config_file, create_link_dict=False
        )
```
### Data post processing
```
   self.post_process()
```
### Filling the template from the read-in data
```
    if self.config_dict:
        suppress_warning = kwargs.pop("suppress_warning", False)
        template.update(
            fill_from_config(
                self.config_dict,
                self.get_entry_names(),
                self.callbacks,
                suppress_warning=suppress_warning,
            )
        )

    return template
```









