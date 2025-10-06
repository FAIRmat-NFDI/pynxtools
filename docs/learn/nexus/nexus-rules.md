# Rules for storing data in NeXus

There are several rules which apply for storing single data items in NeXus. There exists a [summary](https://manual.nexusformat.org/datarules.html) in the NeXus documentation outlining most of these rules. However, to guide data providers even further, we have compiled here additional information and explanations.

## Name resolution

In general, the names of NeXus group and field items are validated according to the boundaries outlined in the [Rules for Storing Data Items in NeXus Files](https://manual.nexusformat.org/datarules.html), section "NXDL group and field names":

- Recommended names
    - lower case words separated by underscores and, if needed, with a trailing number

- Allowed names
    - any combination of upper and lower case letter, numbers, underscores and periods, except that periods cannot be at the start or end of the string
    - This statement is equivalent to matching  this regular expression (named `validItemName` in the [nxdl.xsd](https://github.com/nexusformat/definitions/blob/main/nxdl.xsd) XML Schema file):

      ```regex
      ^[a-zA-Z0-9_]([a-zA-Z0-9_.]*[a-zA-Z0-9_])?$
      ```

- Invalid names:
    - any name not matching this `validItemName` regular expression

Note that this explicitly also means that it is not allowed to have whitespace (including " ") in NeXus names.

A specialty of NeXus is the possibility to define concept names that are different to the names
of the actual data instances. In NeXus base classes and application definitions, there are three options for defining how instances must be named to match to the name of a given concept.
This matching is based on a combination of the `name` and the `nameType` attributes
of the concept.

!!! info "Concept and instance names"
    In NeXus, we must distinguish carefully between names of concepts and the names given to the actual instance of that concept.

    - **Concept Name:** This is the name given to a NeXus concept, i.e., on the data modelling level in the NeXus definitions.
    - **Instance Name:** This is the actual name for a NeXus data instance of the concept (e.g., in an HDF5 file).

There are three different options for the `nameType` XML attribute:

- `specified`
- `any`
- `partial`

If `nameType=specified`, that means that any instance must have the exact same (**fixed**) name as the concept. As an example, if there is a field called `my_field` with `nameType=specified` in an application definition, the only allowed name in a file would be `my_field`. Note that this is also true for concept names containing uppercase letters. "specified" is the default `nameType`, i.e., if no `nameType` is given, it is assumed that any instance name must match the
concept name directly

In addition, there is also the option to allow for **selectable** names. This is achieved by `nameType=any` or `nameType=partial`.

If the `nameType` is any, that means that the concept name can be matched by _any_ instance name, as long as it matches the regular expression above. As an example. As an example, if a field in an application definition is called `FIELD` and has `nameType=any`, `field`, `field0`, `any_other_name` would be allowed names, while `any other name` would not be allowed.

There is also the possibility to fix a _subpart_ of the name using `nameType=partial`. In this case, it important which characters in the concept name are lowercase and which are uppercase. Those characters that are uppercase may be replaced by any other string, as long as the final instance name is still valid according to the regex above. For example, there might be a `userID` group. In this case, allowed names include any name that start with `user`, e.g., `user0`, `user_abcde`,  Note that here it is also allowed to write `user`, i.e., replacing the uppercase part of the name with an empty string.

The validation of names is performed by **namefitting**, i.e., fitting the name that is used by the data provider to the name given in the base class / application definitions.

A python implementation of this process can be found in [this function](https://github.com/FAIRmat-NFDI/nexus_definitions/blob/34aed4a74b8d2a682eb0b9292055dc00e5e0220e/dev_tools/utils/nxdl_utils.py#L112). This function returns twice the length for an exact match, otherwise the number of matching characters (case insensitive) or zero, if `name_any` is set to True, is returned. This is also the function that is used in the [validation](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/validation.py) implemented in `pynxtools`.

## Special rules for names and namefitting

Aside from these general rules, there are a number of special rules for NeXus names that need to be considered:

- There is a set of prefixes (like `BLUESKY_`, `DECTRIS_`, `IDF_`, etc.) that are reserved for certain projects and communities. These prefixes (typically written as uppercase + underscore cannot be overwritten by namefitting.

- There is also a set of reserved suffixes that are used to give additional information for a group or field. These can only be used if the original field is present as well. As an example, the field `temperature_set` - which uses the suffix `_set`, reserved for setpoint of field values - can only be present if the field `temperature` is present as well.

- Additionally to namefitting, data annotation can use further information. For example, in case of NXdata, the axes listed among the `@axes` shall fit to any instances of `AXISNAME` and data objects listed in `@signal` or `@auxiliary_signals` shall fit to instances of `DATA`. Such rules are typically given in the base classes (e.g., see [here](https://manual.nexusformat.org/classes/base_classes/NXdata.html#index-0) for NXdata). Any tool that makes use of the base classes should implement these special rules in its validation procedure. As an example, pynxtools has a special [function for handling NXdata](https://github.com/FAIRmat-NFDI/pynxtools/blob/474fe823112b8ee1e7b42ac80bb7408fdde22bd5/src/pynxtools/dataconverter/validation.py#L220).

For the full list of these respective rules, see [Rules for Storing Data Items in NeXus Files](https://manual.nexusformat.org/datarules.html).

## Concept name inheritance

Note that NeXus also supports inheritance of concepts. The same rules as for instance names on the data level apply here for the inherited concept names. That is, the name of a concept must match in concept name and `nameType` to inherit from another concept. As an example, if we define a field with name `userID` and `nameType="partial"` in a base class and then use this base class in an application definition, the concept `user` and `nameType="specified"` would inherit its property. Contrarily, the concept `my_user` would not inherit from `userID`.