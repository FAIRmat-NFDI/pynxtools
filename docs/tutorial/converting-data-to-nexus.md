# Converting research data to NeXus

## Who is this tutorial for?

The document is for people who want to standardize their research data by converting their research data into
a NeXus standardized format.
We cover the basic principles and common principles of NeXus, here.
For a more detailed description on the general principles of NeXus we recommend reading our
[learning page for NeXus](../learn/nexus-primer.md) or the [official NeXus user manual](https://manual.nexusformat.org/user_manual.html).

## What should you should know before this tutorial?

- You should have a basic understanding of NeXus - [A primer on NeXus](../learn/nexus-primer.md)
- You should have a basic understanding of [FAIR data](https://www.nature.com/articles/sdata201618)

## What you will know at the end of this tutorial?

You will have

- a basic understanding how to use the NeXus data converter from the pynxtools package

## Setup

We use a Python tool to make converting our research data easier. This has a number of [readers](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/pynxtools/dataconverter/readers) that support multiple file formats. You can browse the separate folders to find the reader that might work for you. A generic reader is the [JSON Map Reader](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/pynxtools/dataconverter/readers/json_map).

We will use the [XPS Reader](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/pynxtools/dataconverter/readers/xps) with a [SpecsLabProdigy](https://www.specs-group.com/nc/specs/products/detail/prodigy/) file (.sle) as an example.

#### Steps

1. Download the example files from here: [Example files](https://download-directory.github.io/?url=https://github.com/FAIRmat-NFDI/pynxtools/tree/master/examples/xps)
2. **Extract** the zip and copy the files in your current working directory. You can find the working directory by typing the following in your terminal:
```console
pwd
```
3. Install [pynxtools](https://github.com/FAIRmat-NFDI/pynxtools/tree/master?tab=readme-ov-file#installation)
```console
pip install git+https://github.com/FAIRmat-NFDI/pynxtools.git
```
4. Verify you can run the ```dataconverter``` in a terminal window. Open a terminal with the Python environment where you installed ```pynxtools```. Then type the following:
```console
dataconverter --help
```

## Converting the example files

Once you have your files copied into the working directory. Your directory structure should look like this:
```
├── README.md
├── EX439_S718_Au.sle
├── params.yaml
└── eln_data_sle.yaml
```

Next, you will run the conversion routine from your Python environment:
```console
dataconverter --params-file params.yaml
```

Here we use a params.yaml parameter file to configure the converter. You can try out [other examples from pynxtools](https://github.com/FAIRmat-NFDI/pynxtools/tree/documentation/examples)

This will create a file called ```Au_25_mbar_O2_no_align.nxs``` in your current directory.

**Congrats! You now have a FAIR NeXus file!**
