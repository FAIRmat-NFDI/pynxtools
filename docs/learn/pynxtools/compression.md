# Using compression within HDF5 files 

## Approach

Data compression covers methods to effectively reduce the size of a dataset or portions of it. Lossless and lossy methods are distinguished. There is an entire research field working on developing methods and implementations for each method. Given that `pynxtools` writes its content to HDF5 files, we have decided to use the functionalities that this library provides to motivate users to use compression as an optional feature at the individual dataset level. To preserve the original data we decided to support only with lossless compression algorithms. We also decided to currently not compress strings and scalar dataset.

Specifically, we use the build-in [gzip (deflate) compression filter](https://support.hdfgroup.org/documentation/hdf5-docs/hdf5_topics/UsingCompressionInHDF5.html) due to its wide support across the most frequently used programming languages. Users should be aware that using deflate instead of more modern algorithms has the trade-off that there is as of now no efficient multi-threaded implementation of the compression filter within the HDF5 library. Therefore, compression can take a substantial amount of the total execution time within the `dataconverter` HDF5 file writing part.

## How to use compression

Developers of plugins for `pynxtools` instruct the writing of data via adding variables such as numpy or xarrays

```
array = np.zeros((1000,), np.float64)
```

to specific places in the `template` dictionary object that the `dataconverter` provides. An example follows:

```
template["/ENTRY[entry1]/numpy_array"] = array
```

For such instruction, the `dataconverter` creates an HDF5 dataset instance that uses the so-called contiguous data storage layout. This dataset is not compressed.

Instead, compression can be instructed via a slight modification of the previous example:

```
template["/ENTRY[entry1]/array"] = {
  "compress": array,
  "strength": 9,
}
```

Wrapping the `array` into a dictionary will instruct the `dataconverter` to store a lossless compressed version of the dataset.
The dictionary has one mandatory keyword `compress` surplus one optional keyword `strength`. The latter can be used to overwrite the
default compression strength to trade-off processing time with file size reduction at the granularity of an individual dataset.

Using compression, internally forces the HDF5 library to use a different, a so-called chunked data storage layout.
A chunked data layout can be understood as an internal splitting of the dataset into chunks, pieces that get compressed individually,
typically one after another.

## Benefits for users
The compression filters in HDF5 work in two directions - compression and decompression. Decompression is typically faster than compression.
Thanks to functionalities of `h5py` users can work as conveniently with HDF5 files that combines contiguous and chunked datasets.

The benefit for users is that depending on the entropy of the data, using compression can yield a substantial reduction of the HDF5 file size and thus offers
savings in storage space and data transfer times. Clearly, a downside of using compression is that before any data can be accessed and worked, decompressing
is required. Here, the chunked storage layout offers benefits, as it allows a selective decompression of only those portions required.
This is an effective lever to use when implementing more effective data processing pipelines, especially when not all data are used.

## Expectation management
Compression is often very effective for spectra where data are stored using integer values as for many bins or pixels no counts are taken or
the number of counts is substantially lower the maximum number of counts an integer of a certain precision discretizes.
Compression is often observed less effective for floating point data mainly that when these come from measurements
physically insignificant changes in the last digits still demand storage in lossless compression schemes.
The often smaller precision requirements or precision offered by a measurement in relation to the maximum precision of the datatype,
i.e., discretization used was the motivation for developing lossy compression methods and using lower precision floating point number
e.g., in the field of machine learning and artificial intelligence applications. 

<!--
## Configuring low-level buffers and chunking
Internally, buffers are managed by the HDF5 library to make this process efficiency but also can cause
unexpected extra time spent when the chunking and buffer settings are not calibrated well. Low-level settings and defaults of the
`h5py` Python library as it is used by `pynxtools` surplus low-level settings within the HDF5
library control these these buffers and the chunking itself.-->

