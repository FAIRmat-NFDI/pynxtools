# ELN generator
This is a helper tool for generating ELN files that can be used to add metadata to the dataconverter routine.
Two types of ELN are supported (by passing the flag `eln-type`):
- [**eln**]: The simple ELN generator that can be used in a console or jupyter-notebook.
- [**scheme_eln**]: Scheme based ELN generator that can be used in NOMAD and the ELN can be used as a custom scheme in NOMAD.

```
$ generate_eln --options <value>

Options:
  --nxdl TEXT                  Name of NeXus definition without extension
                               (.nxdl.xml).  [required]
  --skip-top-levels INTEGER    To skip upto a level of parent hierarchical structure.
                               E.g. for default 1 the part Entry[ENTRY] from
                               /Entry[ENTRY]/Instrument[INSTRUMENT]/... will
                               be skiped.  [default: 1]
  --output-file TEXT           Name of  output file.
  --eln-type [eln|scheme_eln]  Choose a type of ELN output (eln or scheme_eln).  [required]
  --help                       Show this message and exit.
```
