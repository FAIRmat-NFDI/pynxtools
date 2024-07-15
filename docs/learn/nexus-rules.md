# Rules for storing data in NeXus

!!! danger "Work in progress"

There are several rules which apply for storing single data items in NeXus. There exists a [summary](https://manual.nexusformat.org/datarules.html) in the NeXus documentation outlining most of these rules. However, this explanation is not exhaustive and thus, we have compiled here additional information.


## Namefitting

In general, the names of NeXus group and field items are validated according to these boundaries:
- Recommended names
  - lower case words separated by underscores and, if needed, with a trailing number

- Allowed names
  - any combination of upper and lower case letter, numbers, underscores and periods, except that periods cannot be at the start or end of the string
  - This statement is equivalent to matching  this regular expression (named `validItemName` in the [nxdl.xsd](https://github.com/nexusformat/definitions/blob/main/nxdl.xsd)) XML Schema file:
  ```
  ^[a-zA-Z0-9_]([a-zA-Z0-9_.]*[a-zA-Z0-9_])?$
  ```
- Invalid names:
  - any name not matching this `validItemName` regular expression

Note that this explicitly also means that it is not allowed to have whitestrings " " in NeXus names.

In NeXus base classes and application definitions, there are two options for defining a concept name. If the group or field in the definition is lowercase, that means that any instance must have the exact same (**fixed**) name. As an example, if there is a field called `my_field` in an application definition, the only allowed name in a file would be `my_field`.

Aside from this lower case notation, there is also the option to allow for **selectable** names. This is achieved by uppercase notation. As an example, if a field in an application definition is called `FIELD`, the name can be any name as long as it maches the regular expression above. For example, `field`, `field0`, `any_other_name` would be allowed names, while `any other name` would not be allowed.

There is also the possibility of mixed lowercase and uppercase notation in base classes and application definitions. For example, there might be a `userID(NXuser)` group. In this case, allowed names include any name that start with `user`, e.g., `user0`, `user_abcde`, as long as the part that replaces the docstring is still valid according to the regex above. Note that here it is also **not** allowed to write `user` without replacing the uppercase part of the name.

The validation of names is performed by **namefitting**, i.e., fitting the name that is used by the data provider to the name given in the base class / application definitions.

A python implementation of this process can be found in [this function](https://github.com/FAIRmat-NFDI/nexus_definitions/blob/34aed4a74b8d2a682eb0b9292055dc00e5e0220e/dev_tools/utils/nxdl_utils.py#L112). This function returns twice the length for an exact match, otherwise the number of matching characters (case insensitive) or zero, if `name_any` is set to True, is returned. This is also the function that is used in the [validation](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/validation.py) implemented in pynxtools.