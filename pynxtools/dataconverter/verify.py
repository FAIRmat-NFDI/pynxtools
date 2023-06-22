"""Verifies a nxs file"""
import os
import sys
from typing import Dict, Union
import click
import xml.etree.ElementTree as ET
import logging
from h5py import File, Dataset, Group

from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.template import Template
from pynxtools.nexus import nexus

logger = logging.getLogger(__name__)

DEBUG_TEMPLATE = 9
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


@click.command()
@click.argument("file")
def verify(file: str):
    """Verifies a nexus file"""
    def_map: Dict[str, str] = {}
    with File(file, "r") as h5file:
        for entry in h5file.keys():
            if h5file[entry].attrs.get("NX_class") == "NXentry":
                def_map = {
                    entry: (
                        definition := h5file[f"/{entry}/definition"][()].decode("utf8")
                    )
                }
                logger.debug(f"Reading entry '{entry}': {definition}'")

    for entry, nxdl in def_map.items():
        definitions_path = nexus.get_nexus_definitions_path()
        nxdl_path = os.path.join(
            definitions_path, "contributed_definitions", f"{nxdl}.nxdl.xml"
        )
        if not os.path.exists(nxdl_path):
            nxdl_path = os.path.join(
                definitions_path, "applications", f"{nxdl}.nxdl.xml"
            )
        if not os.path.exists(nxdl_path):
            raise FileNotFoundError(f"The nxdl file, {nxdl}, was not found.")

        nxdl_root = ET.parse(nxdl_path).getroot()

        ref_template = Template()
        data_template = Template()
        helpers.generate_template_from_nxdl(nxdl_root, ref_template)

        logger.log(DEBUG_TEMPLATE, "Reference template: %s", ref_template)

        class_map: Dict[str, str] = {}

        def replace_group_names(path: str):
            for nx_class in class_map:
                if f"/{nx_class}/" in path or path.startswith(f"{nx_class}/"):
                    path = path.replace(
                        f"{nx_class}/", f"{class_map[nx_class]}[{nx_class}]/"
                    )
            return path

        def collect_entries(name: str, dataset: Union[Group, Dataset]):
            clean_name = replace_group_names(name)
            if isinstance(dataset, Group) and (
                nx_class := dataset.attrs.get("NX_class")
            ):
                entry_name = name.rsplit("/", 1)[-1]
                clean_nx_class = nx_class[2:].upper()

                is_variadic = True
                clean_name = replace_group_names(name)
                for ref_entry in ref_template:
                    if ref_entry.startswith(f"{entry_path}/{clean_name}"):
                        is_variadic = False
                        break

                if is_variadic:
                    class_map[entry_name] = clean_nx_class
                logger.debug("Adding class %s to %s", clean_nx_class, entry_name)

            if isinstance(dataset, Dataset):
                logger.debug("Adding field %s/%s", entry_path, clean_name)
                if isinstance(read_data := dataset[()], bytes):
                    read_data = read_data.decode("utf-8")
                data_template[f"{entry_path}/{clean_name}"] = read_data

            for attr_name, val in dataset.attrs.items():
                if attr_name == "NX_class":
                    continue
                logger.debug(
                    "Adding attribute %s/%s/@%s", entry_path, clean_name, attr_name
                )
                data_template[f"{entry_path}/{clean_name}/@{attr_name}"] = val

        entry_path = f"/ENTRY[{entry}]"
        with File(file, "r") as h5file:
            h5file[f"/{entry}"].visititems(collect_entries)

        logger.debug("Class map: %s", class_map)
        logger.log(DEBUG_TEMPLATE, "Processed template %s", data_template)
        helpers.validate_data_dict(ref_template, Template(data_template), nxdl_root)

        logger.info(
            f"The entry `{entry}` in file `{file}` is a valid file"
            f" according to the `{nxdl}` application definition."
        )
