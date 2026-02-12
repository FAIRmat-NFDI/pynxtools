# Using compression with HDF5 

## Approach

Data compression covers methods to effectively reduce the size of a dataset or portions of it. Lossless and lossy methods are distinguished. There is an entire research field working on developing methods and implementations for each method. Given that `pynxtools` writes its content to HDF5 files, we have decided to use the functionalities that this library provides to motivate users to use compression as an optional feature, at an optionally individual dataset level. To preserve the original data, we decided to support only with lossless compression algorithms. We also decided to currently not compress strings and scalar dataset.

Specifically, we use the build-in [gzip (`deflate`) compression filter](https://support.hdfgroup.org/documentation/hdf5-docs/hdf5_topics/UsingCompressionInHDF5.html) due to its wide support across the most frequently used programming languages. Users should be aware that using `deflate` instead of more modern algorithms has the trade-off that there is as of now no efficient multi-threaded implementation of this compression filter within the HDF5 library. Therefore, compression can take a substantial amount of the total execution time within the `dataconverter` HDF5 file writing part.

## How to use compression

Developers of plugins for `pynxtools` instruct the writing of data via adding variables such as numpy or xarrays like the following example

```
array = np.zeros((1000,), np.float64)
```

to specific places in the `template` dictionary object that the `dataconverter` provides:

```
template["/ENTRY[entry1]/numpy_array"] = array
```

For such an instruction, the `dataconverter` creates an HDF5 dataset instance that uses the so-called contiguous data storage layout. This dataset is stored uncompressed.

As an alternative, compression can be instructed via a slight modification of the previous example:

```
template["/ENTRY[entry1]/array"] = {
  "compress": array,
  "strength": 9,
}
```

Wrapping the `array` here into a dictionary instructs the `dataconverter` to store a lossless compressed version of the same dataset.
The dictionary has one mandatory keyword `compress`. An additional, optional keyword `strength`, exists with which to overwrite the
default compression strength to trade-off processing time with file size reduction at the granularity of an individual dataset.

Using compression internally forces the HDF5 library to use a different, a so-called chunked data storage layout.
A chunked data layout can be understood as an internal splitting of the dataset into chunks, pieces that get compressed individually;
typically one after another.

## Benefits for users

The compression filters in HDF5 work in two directions - compression and decompression. Decompression is typically faster than compression.
Thanks to functionalities offers by `h5py`, users can work as conveniently with HDF5 files irrespective if these combine contiguous and chunked datasets in the same file.

Compared to wrapping the entire HDF5 file into an archive, e.g., when `zip`ping it up, offers more fine-grained control.
Note that especially for a usage in research data management systems, like NOMAD, combining both approaches, wrapping an HDF5 file
that has internally compressed datasets into a zip file is often not additionally effective unless, the HDF5 file has a considerable
number of groups and additional internal datasets where much padding bytes were added internally by the HDF5 library when writing file.

The benefit of using compression for users is that depending on the entropy of the data a substantial reduction of the HDF5 file size and thus savings
in terms of storage space and data transfer times are possible without loosing precision. Clearly, a downside of using compression is that before
any data can be accessed and worked with, e.g., in NOMAD decompressing is required. Thanks to `h5py` functionalities this happens automatically.
The chunked storage layout is useful in that it enables a selective decompression of only those portions of the dataset required.
This is an effective but advanced lever to use when implementing more effective data processing pipelines, especially when not all data are used,
and irrespective of the research data management system or downstream applications that consume the HDF5 file.

## Expectation management

Compression is often very effective for images and spectra where data are stored using integer values as for many bins or pixels no counts are taken or
the number of counts is substantially lower than the maximum number of counts that an integer offers discretization.
Compression is often observed as less effective when applied on floating point data. Frequently this is the case for measurements or simulations
where physically insignificant changes in the last digits still demand for storage when using lossless compression schemes.
The often smaller precision requirements or physical precision offered by a measurement in relation to the maximum precision of the datatype,
i.e., discretization, is the motivation behind developing lossy compression methods and using lower precision floating point numbers
e.g., in the field of machine learning and artificial intelligence. 


## Configure the chunking

While efficient and effective for performing compression tasks, the design of using chunks has also drawbacks that can affect read and write
performance. Consequently, the efficiency and speed with which such chunked and compressed data can be used in downstream processing
and visualization depends on the configuration of the chunks. This is a field where compromises need to be made especially for large datasets.
The `h5py` library implements a heuristic that tries to construct chunks with shape similar to that of the original dataset.
Each chunk is effectively a shrunk (hyper)-rectangle/-cuboid of the original dataset. This pleases users with needs to slice about equally
frequently across all perpendicular viewing directions.

However, there are often cases where there is a clear bias towards slicing across a prioritized direction paired with the expectation
that displaying should be fast when slicing perpendicular to this direction. In this case, it can be useful to overwrite the `h5py` heuristic
with another one which favors that direction by shaping the chunks differently.

As an example, assume you wish to inspect an image stack with 100,000 images each having 1024 x 1024 pixels.
Assume further for simplicity that these pixels are organized in a three-dimensional array that is 100,000 images deep.
Depending on the data layout in memory, the values for the pixels of the same image pack closer in memory than for pixels of neighboring images.
Assume now you wish to inspect primarily one image at a time, i.e. you slice perpendicular to the
image id axis. In this case, it would be ideal to load only the 1024 x 1024 pixels you need and ideally these should be in the same chunk.
Loading neighboring images, or portions of it, speculatively is what modern hardware does and sophisticated visualization software offers,
as it brings advantages when navigating forwards and backwards along the slicing direction.
Assume another user who is interested in seeing the contrast changes along the image id direction, i.e. narrowing on a single pixel column
interested in displaying an array with 100,000 entries. That user would like to have all contrast values again ideally in one chunk and
read-out in one operation. Such use cases can collide substantiating why the optional functionality of `pynxtools` to customize the
chunk settings should be used when there is clear bias towards one particular viewing direction.

Observing that our exclusive relying on the heuristic of `h5py` delivered frequently too small chunks that increased loading and display times
for HDF5 files that were generated with `pynxtools` using H5Web in the NOMAD research data management system. This motivated adding the
here described customization option.

The customization of the chunking heuristic has an additional level of hardware-dependent complexity though. Specifically, the actual
read-out performance of chunked HDF5 content can heavily depend on the file system architecture and its settings. It is important to understand
that the chunk configuration though is defined upon writing dataset into the HDF5 file and cannot be changed thereafter.
The `src/pynxtools/dataconverter/chunk_cache.py` configuration makes explicit typical default values one can use for starting analyses
on different file systems used for deploying NOMAD. By default, we follow the default of the `h5py` library, which tries to achieve a
performance compromise that is tailored towards single storage operations like on servers and laptops.

Developers that customize for Lustre or GPFS based hardware and NOMAD deployments can use the chunk_cache settings to explore further
optimization routes to make the most out of their NeXus/HDF5-file-based RDM pipeline in NOMAD.


