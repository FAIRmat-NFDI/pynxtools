# Using compression with HDF5

## Approach

Data compression covers methods to effectively reduce the size of a dataset or portions of it. Lossless and lossy methods are distinguished. Given that `pynxtools` writes its content to HDF5 files, we have decided to use compression filters that the HDF5 library provides. Using compression or not in `pynxtools` is optional. The user can decide at the individual dataset level. To preserve the original data, we decided to only support lossless compression algorithms. We also decided to not compress strings and scalar datasets.

Specifically, we use the build-in [`deflate` compression filter](https://support.hdfgroup.org/documentation/hdf5-docs/hdf5_topics/UsingCompressionInHDF5.html) due to its wide support across the most frequently used programming languages. Users should be aware that using `deflate` instead of more modern algorithms has the trade-off that there is as of now no efficient multi-threaded implementation of this compression filter within the HDF5 library. Therefore, compression can take a substantial amount of the total execution time within the `dataconverter` HDF5 file writing part.

## How to use compression

Developers of plugins for `pynxtools` instruct the writing of data by adding variables such as numpy arrays or xarrays like


```
array = np.zeros((1000,), np.float64)
```

to specific places in the [`template`](https://fairmat-nfdi.github.io/pynxtools/how-tos/pynxtools/build-a-plugin.html#the-reader-template-dictionary) object that the `dataconverter` provides:

```
template["/ENTRY[entry1]/numpy_array"] = array
```

Given such a template entry, the `dataconverter` creates an HDF5 dataset instance that uses the so-called contiguous data storage layout. That means that the dataset is stored uncompressed.

As an alternative, compression can be instructed via a slight modification of the previous example:

```
template["/ENTRY[entry1]/array"] = {
  "compress": array,
  "strength": 9,
}
```

Wrapping the `array` here into a dictionary instructs the `dataconverter` to store a lossless compressed version of the same dataset.
The dictionary has one mandatory keyword `compress`. An additional, optional keyword `strength` exists which can be used to overwrite the
default compression strength to trade-off processing time with file size reduction at the granularity of an individual dataset.

Using compression internally forces the HDF5 library to use a different, so-called chunked data storage layout.
A chunked data layout can be understood as an internal splitting of the dataset into chunks, pieces that get compressed individually;
typically one after another.

## Benefits for users

The compression filters in HDF5 work in two directions - compression and decompression. Decompression is typically faster than compression.
Using functionalities offered by `h5py`, users can work as conveniently with HDF5 files irrespective even when combining contiguous and chunked datasets in the same file.

Compared to wrapping the entire HDF5 file into an archive, e.g., when `zip`ping it up, chunking offers more fine-grained control.
Often when uploading content to research data management systems, like NOMAD, users wrap their file(s) into a `zip` or other types of compressed archives. Using compression as described above can often make this obsolete as improvements of additional compression are insignificant. A relevant exception where `zip`ping an HDF5 file is still useful although much of its internal content has already been compressed is when there is a considerable number of groups surplus substantial padding bytes remaining.

Using compression can significantly reduce the size of HDF5 files, depending on the entropy of the data. This leads to savings in storage requirements and faster data transfer, without any loss of numerical precision. Clearly, a downside of using compression is that before
any data can be accessed and worked with, e.g., in NOMAD, decompressing is required; `h5py` does this automatically.
The chunked storage layout is useful in that it enables a selective decompression of only those portions of the dataset required.
This provides an effective, but more advanced, mechanism, for improving data processing pipelines, particularly when only subsets of the data are required, and independently of the research data management system or downstream applications that access the HDF5 file.

## Expectation management

Compression is often very effective for images and spectra where data are stored using integer values as for many bins or pixels no counts are taken or
the number of counts is substantially lower than the maximum value that the integer type can represent.
Compression is often observed as less effective when applied on floating point data. Frequently this is the case for measurements or simulations
where physically insignificant changes in the last digits still demand for storage when using lossless compression schemes.
The often smaller precision requirements or physical precision offered by a measurement in relation to the maximum precision of the datatype,
i.e., discretization, is the motivation behind developing lossy compression methods and using floating point numbers with a lower precision
as those frequently used by machine learning and artificial intelligence frameworks.

## Tailoring the chunking

While efficient and effective for performing compression tasks, the usage of chunks has also drawbacks that can affect performance.
Consequently, the efficiency and thus processing speed that compressed data offer when used in downstream processing and visualization depends
on the configuration of the chunks. Compromises need to be made especially for large datasets. The `h5py` library uses a heuristic to generate
chunk shapes that resemble the dimensions of the original dataset. This serves users that slice a datasets approximately equally
frequently across all perpendicular viewing directions.

However, there are often cases where one of the viewing directions is prioritized and users expect that displaying should be fastest when
slicing perpendicular to this direction. In this case, it can be useful to overwrite the `h5py` heuristic
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
here described customization option. For technical details we refer to the [implementation](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/chunk.py).

## Customizing chunk settings for different file systems

The customization of the chunking heuristic has an additional level of hardware-dependent complexity though. Specifically, the actual
read-out performance of chunked HDF5 content can heavily depend on the file system architecture and its settings. It is important to understand
that the chunk configuration though is defined upon writing dataset into the HDF5 file and cannot be changed thereafter.
The `src/pynxtools/dataconverter/chunk.py` configuration makes explicit typical default values one can use for starting analyses
on different file systems used for deploying NOMAD. By default, we follow the default of the `h5py` library, which tries to achieve a
performance compromise that is tailored towards single storage operations like on servers and laptops.

Developers that customize for Lustre or GPFS based hardware and NOMAD deployments can use the chunk_cache settings to explore further
optimization routes to make the most out of their NeXus/HDF5-file-based RDM pipeline in NOMAD.

## Judicious choices when using custom compression filters

To maximize the reusability of all NeXus/HDF5 files, we have intentionally chosen to use `deflate` as the default compression algorithm and respective HDF5 compression filter (`gzip` in `h5py`) in `pynxtools`. The HDF5 library integrates and links the source code of this widely supported algorithm naturally
during its compilation step for important programming languages like Fortran, C, C++, Matlab, and Python. Through its `compression="gzip"` parameter, the algorithm is straightforward to use with `h5py`. Also `pynxtools` uses this approach in its `src/pynxtools/dataconverter/writer.py` backend.

An important practical issue, though, of the `deflate` compression filter is that currently no multithreaded implementation of this filter exists in the HDF5 library. We have observed that this enforced sequentialization of compression becomes a substantial performance bottleneck in batch processing scenarios
and for data ingestion campaigns with research data management systems like NOMAD. Therefore, users should always judge if using
compression yields relevant and measurable benefits such as reduced storage costs. Informed decision making is required as different filters fit better or worse certain use cases. While compression may reduce storage cost it is important to mention that working with compressed content incurs an overhead that is paid whenever compressed content needs processing and displaying. Therefore, `pynxtools` offers now to combine different optimizations like compression, different compression filters, all optionally usable at the individual dataset level to care for a number of use cases.

Consequently, the feature of `pynxtools` to support also filters from the [`blosc2`](https://blosc.org/)
project and compression library via [`hdf5plugin`](https://pypi.org/project/hdf5plugin/) is an offering to our users with
performance critical processing demands. We have configured `blosc` such that if used, we work with the `zstd` compression algorithm.
This custom compression filter has a multithreaded and vectorized implementation, two key optimizations over `deflate` that make it an attractive alternative
for users with demands for processing large data volume. By default, the usage of `blosc` is switched off. Users interested in this feature should for now create a custom feature branch for `pynxtools` and switch on `PYNX_ENABLE_BLOSC = True` in `src/pynxtools/dataconverter/chunk.py`.

However, users should be aware that custom compression filters, like `blosc2`, are not typically included in the default compilation pipelines of HDF5.
This means that NeXus/HDF5 files with datasets that use these filters will have content that is typically not readable in C, C++, Fortran, or Matlab applications, unless the filter also gets specifically compiled and linked into the respective installation of the HDF5 library.
Also standalone HDF5 file viewers like [`HDFView`](https://www.hdfgroup.org/download-hdfview/) do not support displaying such content out-of-the-box.
When `pynxtools` is installed in a NOMAD deployment, newer versions of `H5Web` are able to display such content. As for every compressed
dataset in HDF5, using a chunked storage layout is mandatory. Chunks will be decompressed prior displaying any content by `H5Web` and `h5py` calls automatically.

## Judicious choices when using multithreaded compression filters


Another consideration to make when using multithreaded compression filters is to set the maximum number of threads which the filter is allowed to use.
Currently, `pynxtools` makes a conservative choice in that it takes half of the available hardware cores on the system. For Intel based CPUs this counts hyperthreading cores in. Like the `PYNX_ENABLE_BLOSC` variable, users can customize these settings on their feature branch by configuring the respective `PYNX_ENABLE_BLOSC_NTHREADS` global in `src/pynxtools/dataconverter/writer.py`. Increasing the number of threads often increases the speed with which compression filters work. Again, informed decisions are required, though, as using multiple threads may result in situation where these threads compete with other threads and processes for requesting resources on the host.
