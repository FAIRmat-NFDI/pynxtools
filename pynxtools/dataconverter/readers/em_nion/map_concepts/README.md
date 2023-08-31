## Scope

Here we store the json dictionaries whereby the parser identifies if a certain
nionswift display_item can be mapped to an available logical NeXus concept.

The dictionary is very similar to the approach taken by the jsonmap_reader.
However the order of the dictionary is reversed. Namely, the keys of the dictionary
identify specific names in the json metadata dictionary representation of nionswift.
The left (value) part of the dictionary is a tuple of a string giving the corresponding
variadic (template) path in NXem onto which a value is mapped, the second value in the
tuple is numpy.dtype, if that value is str only then there is a third entry
in the tuple which identifies the expected dimensionality of the data.
