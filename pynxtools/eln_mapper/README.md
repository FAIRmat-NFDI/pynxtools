# ELN generator
This is a helper tool for generating eln
- The simple eln generator that can be used in a console or jupyter-notebook
- Scheme based eln generator that can be used in NOMAD and the eln can be used as a custom scheme in NOMAD.

```
$ eln_generator --options <value>

Options:
  --nxdl TEXT                  Name of NeXus definition without extension
                               (.nxdl.xml).  [required]
  --skip-top-levels INTEGER    To skip upto a level of parent hierarchical structure.
                               E.g. for default 1 the part Entry[ENTRY] from
                               /Entry[ENTRY]/Instrument[INSTRUMENT]/... will
                               be skiped.  [default: 1]
  --output-file TEXT           Name of  output file.
  --eln-type [eln|scheme_eln]  Choose a type from the eln or scheme_eln.  [required]
  --help                       Show this message and exit.
```
