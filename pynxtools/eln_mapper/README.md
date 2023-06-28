# ELN generator
This is helper tool for generating eln
- The simple eln generator that can be used in console or jupyter-notebook
- Scheme base eln generator that can be used in nomad and the eln can be used as custom
  scheme in nomad.

```
$ eln_generator --options <value>

Options:
  --nxdl TEXT                  Name of NeXus definition without extension
                               (.nxdl.xml).  [required]
  --skip-top-levels INTEGER    To skip the level of parent hierarchy level.
                               E.g. for default 1 the partEntry[ENTRY] from
                               /Entry[ENTRY]/Instrument[INSTRUMENT]/... will
                               be skiped.  [default: 1]
  --output-file TEXT           Name of file that is neede to generated output
                               file.
  --eln-type [eln|scheme_eln]  [required]
  --help                       Show this message and exit.

```
