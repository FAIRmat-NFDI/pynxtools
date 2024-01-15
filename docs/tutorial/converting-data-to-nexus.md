# Converting research data to NeXus

!!! danger "Work in progress"

    This part of the documentation is still being written and it might be confusing or incomplete.

## Who is this tutorial for?

The document is for people who want to standardize their research data by converting their research data into 
a NeXus standardized format.
We cover the basic principles and common principles of NeXus, here.
For a more detailed description on the general principles of NeXus we recommend reading our 
[learning page for NeXus](../learn/nexus-primer.md) or the [official NeXus user manual](https://manual.nexusformat.org/user_manual.html).

## What should you should know before this tutorial?

- You should have a basic understanding of NeXus - [A primer on NeXus](../learn/nexus-primer.md)
- You should have a basic understanding of FAIR data - [wilkinson et al](...)

## What you will know at the end of this tutorial?

You will have

- a basic understanding how to use the NeXus data converter from the pynxtools package

## Setup

We use a Python tool to make converting our research data easier. This has a number of [readers](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/pynxtools/dataconverter/readers) that support multiple file formats. You can browse the separate folders to find the reader that might work for you. A generic reader is the [JSON Map Reader](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/pynxtools/dataconverter/readers/json_map).

We will use the [XPS Reader](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/pynxtools/dataconverter/readers/xps) with Vamas (.vms) files as an example. 

#### Steps

1. Download the example files from here:
2. Install [pynxtools](https://github.com/FAIRmat-NFDI/pynxtools/tree/master?tab=readme-ov-file#installation)
3. Verify you can run the ```dataconverter``` in a terminal window. Open a terminal with the Python environment where you installed ```pynxtools```. Then type the following:
```console
dataconverter --help
```
4. Copy the example files to your working directory. You can find the working directory by typing the following in your terminal:
```console
pwd
```

## Converting the example files

!!! **we might need a part to explain how to find an appdef to use and link to documents on creating an appdef**

Once you have your files copied into the working directory. Your directory structure should look like this:
```
- file1.vms
- otherfile.vms
```

Next, you will run the conversion routine:
```console
dataconverter --reader xps 
```

This will create a file called ```output.nxs``` in your current directory.

**Congrats! You now have a FAIR NeXus file!**
