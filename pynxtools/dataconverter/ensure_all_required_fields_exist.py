@lru_cache(maxsize=None)
def path_in_data_dict(nxdl_path: str, data_keys: Tuple[str, ...]) -> List[str]:
    """Checks if there is an accepted variation of path in the dictionary & returns the path."""
    found_keys = []
    for key in data_keys:
        if nxdl_path == convert_data_converter_dict_to_nxdl_path(key):
            found_keys.append(key)
    return found_keys


def ensure_all_required_fields_exist(template, data, nxdl_root):
    """Checks whether all the required fields are in the returned data object."""
    check_basepaths = set()
    for path in template["required"]:
        entry_name = get_name_from_data_dict_entry(path[path.rindex("/") + 1 :])
        if entry_name == "@units":
            continue
        nxdl_path = convert_data_converter_dict_to_nxdl_path(path)
        renamed_paths = path_in_data_dict(nxdl_path, tuple(data.keys()))

        if len(renamed_paths) > 1:
            check_basepaths.add(get_concept_basepath(nxdl_path))
            continue

        if not renamed_paths:
            logger.warning(
                f"The data entry corresponding to {path} is required "
                f"and hasn't been supplied by the reader.",
            )
            continue

        for renamed_path in renamed_paths:
            renamed_path = path if renamed_path is None else renamed_path
            if path in template["lone_groups"]:
                opt_parent = check_for_optional_parent(path, nxdl_root)
                if opt_parent != "<<NOT_FOUND>>":
                    if does_group_exist(opt_parent, data) and not does_group_exist(
                        renamed_path, data
                    ):
                        logger.warning(
                            f"The required group, {path}, hasn't been supplied"
                            f" while its optional parent, {opt_parent}, is supplied."
                        )
                    continue
                if not does_group_exist(renamed_path, data):
                    logger.warning(f"The required group, {path}, hasn't been supplied.")
                    continue
                continue
            if data[renamed_path] is None:
                logger.warning(
                    f"The data entry corresponding to {renamed_path} is required "
                    f"and hasn't been supplied by the reader.",
                )

    for base_path in check_basepaths:
        required_fields = get_required_fields_for(base_path)
        paths = get_concept_variations(base_path)

        missing_fields = set()
        partially_present_path = set()
        for path in paths:
            for required_field in required_fields:
                if (
                    f"{path}/{required_field}" not in data
                    or data[f"{path}/{required_field}"] is None
                ):
                    missing_fields.add(f"{path}/{required_field}")

                if data[f"{path}/{required_field}"] is not None:
                    partially_present_path.add(f"{path}")

        for missing_field in missing_fields:
            logger.warning(
                f"The data entry corresponding to {missing_field} is required "
                "and hasn't been supplied by the reader.",
            )
