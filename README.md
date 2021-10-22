This is not a real parser, but an nexus template on how to write one. You can fork this repository to create actual parsers.

## Get started

You should create a virtual environment. This is optional, but highly recommended as
the required nomad-lab pypi package requires many dependencies with specific versions
that might conflict with other libraries that you have installed. This was tested
with Python 3.7.

```
pip install virtualenv
virtualenv -p `which python3` .pyenv
source .pyenv/bin/activate
```

Simply install our pypi package with pip:
```
pip install --upgrade pip
pip install nomad-lab
```

Clone this project (or fork and then clone the fork). Go into the cloned directly and
directly run the parser from there:
```
git clone https://github.com/nomad-coe/nomad-parser-nexus.git parser-nexus
cd parser-nexus
python -m nexusparser tests/data/nexus.out
```

There are also a basic test framework written in [pytest](https://docs.pytest.org/en/stable/).
Install the remaining dev dependencies and run the tests with:
```
pip install -r requirements.txt
pytest -sv tests
```

## Next steps

Our documentation provides several resources that might be interesting:
- [How to write a parser](https://nomad-lab.eu/prod/rae/docs/parser.html). Provides
  a more detailed tutorial on how to write a parser.
- [Introduction to the NOMAD Metainfo](https://nomad-lab.eu/prod/rae/docs/metainfo.html).
  This explains how NOMAD data schema and can be extended and used within your parser.

To get you parser included in NOMAD or ask further questions, you can:
- Use our forums at [matsci.org](https://matsci.org/c/nomad/32)
- Open an issue on the [nexus-parser GitHub project](https://github.com/nomad-coe/nomad-parser-nexus/issues)
- Write to [support@nomad-lab.eu](mailto:support@nomad-lab.eu)

**Note!** The rest of this README.md is the usual text that applies to all NOMAD parsers.


This is a NOMAD parser for [EXAMPLE](https://www.nexus.eu/). It will read EXAMPLE input and
output files and provide all information in NOMAD's unified Metainfo based Archive format.

## Preparing code input and output file for uploading to NOMAD

NOMAD accepts `.zip` and `.tar.gz` archives as uploads. Each upload can contain arbitrary
files and directories. NOMAD will automatically try to choose the right parser for you files.
For each parser (i.e. for each supported code) there is one type of file that the respective
parser can recognize. We call these files `mainfiles` as they typically are the main
output file a code. For each `mainfile` that NOMAD discovers it will create an entry
in the database that users can search, view, and download. NOMAD will associate all files
in the same directory as files that also belong to that entry. Parsers
might also read information from these auxillary files. This way you can add more files
to an entry, even if the respective parser/code might not directly support it.

For EXAMPLE please provide at least the files from this table if applicable to your
calculations (remember that you can provide more files if you want):

|Input Filename| Description|
|--- | --- |
|`nexus.out` | **Mainfile** in EXAMPLE specific plain-text |


To create an upload with all calculations in a directory structure:

```
zip -r <upload-file>.zip <directory>/*
```

Go to the [NOMAD upload page](https://nomad-lab.eu/prod/rae/gui/uploads) to upload files
or find instructions about how to upload files from the command line.

## Using the parser

You can use NOMAD's parsers and normalizers locally on your computer. You need to install
NOMAD's pypi package:

```
pip install nomad-lab
```

To parse code input/output from the command line, you can use NOMAD's command line
interface (CLI) and print the processing results output to stdout:

```
nomad parse --show-archive <path-to-file>
```

To parse a file in Python, you can program something like this:
```python
import sys
from nomad.cli.parse import parse, normalize_all

# match and run the parser
archive = parse(sys.argv[1])
# run all normalizers
normalize_all(archive)

# get the 'main section' section_run as a metainfo object
section_run = archive.section_run[0]

# get the same data as JSON serializable Python dict
python_dict = section_run.m_to_dict()
```

## Developing the parser

Create a virtual environment to install the parser in development mode:

```
pip install virtualenv
virtualenv -p `which python3` .pyenv
source .pyenv/bin/activate
```

Install NOMAD's pypi package:

```
pip install nomad-lab
```

Clone the parser project and install it in development mode:

```
git clone https://github.com/nomad-coe/nomad-parser-nexus.git parser-nexus
pip install -e parser-nexus
```

Running the parser now, will use the parser's Python code from the clone project.

$parserSpecific$
