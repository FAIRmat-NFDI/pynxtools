# The MultiFormatReader as a reader superclass

There are three options for building a new `pynxtools` reader:

1. build the reader from scratch
2. inherit and extend the [**`BaseReader`**](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/base/reader.py)
3. inherit and extend the [**`MultiFormatReader`**](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/multi/reader.py)

While option 1 is generally not recommended, inheriting and extending the `BaseReader` has traditionally been the default solution for all existing pynxtools readers and reader plugins. The `BaseReader`, which is an abstract base class, has an essentially empty ```read``` function and is  thus only helpful for implementing the correct input/output design of the ```read``` function of any reader which is implemented off of it.

While building on the ```BaseReader``` allows for the most flexibility, in most cases it is desirable to implement a reader that can read in multiple file formats and then populate the NeXus file based on the read data, in compliance with a NeXus application definition. For this purpose, `pynxtools` has the [**`MultiFormatReader`**](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/multi/reader.py), which can be readily extended for any new data.

Here, we will explain the inner workings of the `MultiFormatReader`. Note that there is also a [how-to guide](../how-tos/use-multi-format-reader.md) on how to implement a new reader off of the `MultiFormatReader` using a concrete example. In case you simply want to use the `MultiFormatReader` without understanding its inner logic, we recommend you start there.

## The basic structure

For extending the `MultiFormatReader`, the following basic structure must be implemented:

```python title="multi/reader.py"
"""MyDataReader implementation for the DataConverter to convert mydata to NeXus."""
from typing import Any

from pynxtools.dataconverter.readers.base.reader import MultiFormatReader

class MyDataReader(MultiFormatReader):
    """MyDataReader implementation for the DataConverter to convert mydata to NeXus."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.extensions = {
            ".yml": self.handle_eln_file,
            ".yaml": self.handle_eln_file,
            ".json": self.set_config_file,
            # Here, one must add functions for handling any other file extension(s)
        }
# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = MyDataReader
```

In order to understand the capabilities of the `MultiFormatReader` and which methods need to be implemented when extending it, we will have a look at its ```read``` method:

```python title="multi/reader.py"
def read(
    self,
    template: dict = None,
    file_paths: tuple[str] = None,
    objects: Optional[tuple[Any]] = None,
    **kwargs,
) -> dict:
    self.kwargs = kwargs
    self.config_file = self.kwargs.get("config_file", self.config_file)
    self.overwrite_keys = self.kwargs.get("overwrite_keys", self.overwrite_keys)   
```

## Template initialization and processing order

An empty `Template` object is initialized that later gets filled from the data files later.

```python title="multi/reader.py"
    template = Template(overwrite_keys=self.overwrite_keys)

    def get_processing_order(path: str) -> tuple[int, Union[str, int]]:
        """
        Returns the processing order of the file.
        """
        ext = os.path.splitext(path)[1]
        if self.processing_order is None or ext not in self.processing_order:
            return (1, ext)
        return (0, self.processing_order.index(ext))

    sorted_paths = sorted(file_paths, key=get_processing_order)
```

If the reader has a `self.processing_order`, the input files get sorted in this order.
If `self.overwrite_keys` is True, later files get precedent. For example, if `self.processing_order = [".yaml", ".hdf5"]`, any values coming from HDF5 files would overwrite values from the YAML files.

## Reading of input files

```python title="multi/reader.py"
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

This parts reads in the data from all data files. The `MultiFormatReader` has an `extensions` property, which is a dictionary that for each file extension calls a function that reads in data from files with that extension. If the reader shall handle e.g. an HDF5 file, a method for handling this type of file should be added, i.e., `self.extensions[".hdf5"] = self.handle_hdf5`.
Note that these methods should also implement any logic depending on the provided data, i.e., it may not be sufficient to rely on the filename suffix, but the reader may also need to check for different file versions, binary signature, mimetype, etc.

Any of these methods should take as input only the file path, e.g.

```python title="multi/reader.py"
def handle_eln_file(self, file_path: str) -> dict[str, Any]
```

These methods must return a dictionary. One possibility is to return a dictionary that directly fills the template (see the `template.update` call above) with the data from the file. Another option is to return an empty dictionary (i.e., not fill the template at this stage) and only later fill the template from a config file (see below).

Note that for several input formats, standardized parser functions already exist within the `MultiFormatReader`. For example, YAML files can be parsed using the `pynxtools.dataconverter.readers.utils.parse_yml` function.

## Setting default values in the template

```python title="multi/reader.py"
    template.update(self.setup_template())
```

Next, the `setup_template` method can be implemented, which is used to populate the template with initial data that does not come from the files themselves. This may be used to set fixed information, e.g., about the reader. As an example, `NXentry/program_name` (which is defined as the name of program used to generate the NeXus file) scan be set to `pynxtools-plugin` by making `setup_template` return a dictionary of the form

```json
{
  "/ENTRY[my_entry]/program_name": "pynxtools-plugin",
  "/ENTRY[my_entry]/program_name/@version": "v0.1.0"
}
```

## Handling objects

```python title="multi/reader.py"
    if objects is not None:
        template.update(self.handle_objects(objects))
```

Aside from data files, it is also possible to directly pass any Python objects to the `read` function (e.g., a numpy array with measurement data). In order to exploit this, the `handle_objects` method must implemented, which should return a dictionary that populates the template.

## Parsing the config file

```python title="multi/reader.py"
    if self.config_file is not None:
        self.config_dict = parse_flatten_json(
            self.config_file, create_link_dict=False
        )
```

Next up, we can make use of the config file, which is a JSON file that tells the reader which input data to use to populate the template. In other words, the config.json is used for ontology mapping between the input file paths and the NeXus application definition. Essentially, the config file should contain all keys that are present in the NXDL. A subset of a typical config file may look like this:

```json
{
  "/ENTRY/title": "@attrs:metadata/title", 
  "/ENTRY/USER[user]": {
    "name": "my_name",
  }, 
  "/ENTRY/INSTRUMENT[instrument]": {
    "name":"@eln",
    "temperature_sensor": {
      "value": "@attrs:metadata/temp",
      "value/@units": "K"
    }
  },
  "/ENTRY/SAMPLE[sample]": {
    "temperature_env": {
      "temperature_sensor": "@link:/entry/instrument/temperature_sensor"
    }
  },  
  "/ENTRY/data": {
    "@axes": "@data:dims",
    "AXISNAME_indices[@*_indices]": "@data:*.index",
    "@signal": "data",
    "data": "@data:mydata",
  }
}
```

Here, the `parse_flatten_json` method is used that allows us to write the config dict in the structured manner above and internally flattens it (so that it has a similar structure as the Template).

In the config file, one can

1. hard-code values (like the unit `"K"` in `"/ENTRY/INSTRUMENT[instrument]/temperature_sensor/value/@units"`) or
2. tell the reader where to search for data using the `@`-prefixes. For more on these prefixes, see below.

Note that in order to use a `link_callback` (see below), `create_link_dict` must be set to `False`, which means that at this stage, config values of the form `"@link:"/path/to/source/data"` get NOT yet converted to `{"link": "/path/to/source/data"}`.

## Data post processing

```python title="multi/reader.py"
   self.post_process()
```

In case there is the need for any post-processing on the data and/or config dictionary _after_ they have been read, the `post_process` method can be implemented. For example, this can be helpful if there are multiple entities of a given NX_CLASS (for example, multiple detectors) on the same level and the config dict shall be set up to fill the template with all of these entities.

## Filling the template from the read-in data

```python title="multi/reader.py"
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

As a last step, the template is being filled from the config dict using the data. If there is more than one entry, the `get_entry_names` method must be implemented, which shall return a list of all entry names. The `fill_from_config` method iterates through all of the them and replaces the generic `/ENTRY/` in the config file by keys of the form `/ENTRY[my-entry]/` to fill the template.

Here, we are using **callbacks**, which are used to bring in data based on `@`-prefixes in the config file. These are defined in the reader's ``__init__`` call using the `pynxtools.dataconverter.readers.multi.ParseJsonCallbacks` class:

```python title="multi/reader.py"
self.callbacks = ParseJsonCallbacks(
    attrs_callback=self.get_attr,
    data_callback=self.get_data,
    eln_callback=self.get_eln_data,
    dims=self.get_data_dims,
)
```

The `ParseJsonCallbacks` class has an attribute called `special_key_map` that makes use of these callbacks to populate the template based on the starting prefix of the config dict value:

```python title="multi/reader.py"
self.special_key_map = {
    "@attrs": attrs_callback if attrs_callback is not None else self.identity,
    "@link": link_callback if link_callback is not None else self.link_callback,
    "@data": data_callback if data_callback is not None else self.identity,
    "@eln": eln_callback if eln_callback is not None else self.identity,
}
```

That means, if the config file has an entry ```{"/ENTRY/title": "@attrs:metadata/title"}```, the `get_attr` method of the reader gets called and should return an attribute from the given path, i.e., in this case from `metadata/title`.

By default, the MultiFormatReader supports the following special prefixes:

- `@attrs`: To get metadata from the read-in experiment file(s). You need to implement the `get_attr` method in the reader.
- `@data`: To get measurement data from the read-in experiment file(s). You need to implement the `get_data` method in the reader.
- `@eln`: To get metadata from additional ELN files. You need to implement the `get_eln_data` method in the reader.
- `@link`: To implement a link between two entities in the NeXus file. By default, the link callback returns a dict of the form {"link": value.replace("/entry/", f"/{self.entry_name}/")}, i.e., a generic `/entry/` get replaced by the actual `entry_name`.

The distinction between data and metadata is somewhat arbitrary here. The reason to have both of these prefixes is to have different methods to access different parts of the read-in data. For example, `@attrs` may just access key-value pairs of a read-in dictionary, whereas `@data` can handle different object types, e.g. xarrays. The implementation in the reader decides how to distinguish data and metadata and what each of the callbacks shall do.

In addition, the reader can also implement the `get_data_dims` method, which is used to return a list of the data dimensions (see below for more details).

All of `get_attr`, `get_data`, and `get_eln_data`  (as well as any similar method that might be implemented) should have the same call signature:

```python
def get_data(self, key: str, path: str) -> Any:
```

Here, `key` is the config dict key (e.g., `"/ENTRY[my-entry]/data/data"`) and path is the path that comes _after_ the prefix in the config file. In the example config file above, `path` would be `mydata`. With these two inputs, the reader should be able to return the correct data for this template key.

### Special rules

- **Lists as config value**: It is possible to write a list of possible configurations of the sort
  ```json
  "/ENTRY/title":"['@attrs:my_title', '@eln', 'no title']"
  ```
  The value must be a string which can be parsed as a list, with each item being a string itself. This allows to provide different options depending if the data exists for a given callback. For each list item , it is checked if a value can be returned and if so, the value is written. In this example, the converter would check (in order) the `@attrs` (with path `"my_title"`) and `@eln` (with path `""`) tokens and write the respective value if it exists. If not, it defaults to "no title".
  This concept can be particularly useful if the same config file is used for multiple measurement configurations, where for some setup, the same metadata may or may not be available.

    Note that if this notation is used, it may be helpful to pass the `suppress_warning` keyword as `True` to the read function. Otherwise, there will be a warning for every non-existent value.

- **Wildcard notation**: There exists a wildcard notation (using `*`)
  ```json
  "/ENTRY/data/AXISNAME[*]": "@data:*.data",
  ```
  that allows filling multiple fields of the same type from a list of dimensions. This can be particularly helpful for writing `DATA` and `AXISNAME` fields that are all stored under similar paths in the read-in data.
  For this, the `get_data_dims` method needs to be implemented. For a given path, it should return a list of all data axes available to replace the wildcard.
    
    The same wildcard notation can also be used within a name to repeat entries with different names (e.g., field_*{my, name, etc} is converted into three keys with * replaced by my, name, etc, respectively). As an example, for multiple lenses and their voltage readouts, one could write:
  ```json
  "LENS_EM[lens_*{A,B,Foc}]": {
    "name": "*",
    "voltage": "@attrs:metadata/file/Lens:*:V",
    "voltage/@units": "V"
  },
  ```
  which would write `NXlens_em` instances named `lens_A`, `lens_B`, and `lens_Foc`.

- **Required fields in optional groups**: There will sometimes be the situation that there is an optional NeXus group in an application definition, that (if implemented) requires some sub-element. As an example, for the instrument's energy resolution, the only value expected to come from a data source is the `resolution`, whereas other fields are hardcoded.
  ```json
  "ENTRY/INSTRUMENT[instrument]/energy_resolution": {
    "resolution": "@attrs:metadata/instrument/electronanalyzer/energy_resolution",
    "resolution/@units": "meV",
    "physical_quantity": "energy"
  }
  ```
  Now, if there is no data for `@attrs:metadata/instrument/electronanalyzer/energy_resolution` available in a dataset, this will be skipped by the reader, and not available, yet the other entries are present. During validation, this means that the required field `resolution` of the optional group `energy_resolution` is not present, and thus a warning or error would be raised:
  ```console
  LookupError: The data entry, /ENTRY[entry]/INSTRUMENT[instrument]/ELECTRONANALYZER[electronanalyzer]/energy_resolution/physical_quantity, has an optional parent, /ENTRY[entry]/INSTRUMENT[instrument]/ELECTRONANALYZER[electronanalyzer]/energy_resolution, with required children set. Either provide no children for /ENTRY[entry]/INSTRUMENT[instrument]/ELECTRONANALYZER[electronanalyzer]/energy_resolution or provide all required ones.
  ```

    To circumvent this problem, there exists a notation using the `"!"` prefix. If you write
    ```json
    "ENTRY/INSTRUMENT[instrument]/energy_resolution/resolution": "!@attrs:metadata/instrument/electronanalyzer/energy_resolution"
    ```
    the whole parent group `/ENTRY/INSTRUMENT[instrument]/energy_resolution` will _not_ be written in case that there is no value for `@attrs:metadata/instrument/electronanalyzer/energy_resolution"`, thus preventing the aforementioned error.