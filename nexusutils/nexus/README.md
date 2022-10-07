The **nexus.py** tool can be used as a standalone tool  **Testing nexus***

Following example dataset can be used to test `nexus.py` module `tests/data/nexus/201805_WSe2_arpes.nxs`.
This is an angular-resolved photoelectron spectroscopy (ARPES) dataset and it is formatted according to
the [NXarpes application definition of NEXUS](https://manual.nexusformat.org/classes/applications/NXarpes.html#nxarpes).

Run the following command to test the `nexus.py` using example ARPES dataset:
```
python test_parser.py
```

You should get a message reading "Testing of nexus.py is SUCCESSFUL." if everything goes as expected!
