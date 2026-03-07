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
i.e., discretization, is the motivation behind developing lossy compression methods and using lower precision floating point numbers
e.g., in the field of machine learning and artificial intelligence. 


