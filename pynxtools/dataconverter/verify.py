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

        empty_template = Template()
        template = Template(empty_template)
        helpers.generate_template_from_nxdl(nxdl_root, template)

        logger.log(DEBUG_TEMPLATE, "Generated template: %s", template)

        class_map: Dict[str, str] = {}

        def collect_groups(name: str, dataset: Union[Group, Dataset]):
            if isinstance(dataset, Group) and (
                nx_class := dataset.attrs.get("NX_class")
            ):
                entry_name = name.rsplit("/", 1)[-1]
                clean_nx_class = nx_class[2:].upper()

                class_map[entry_name] = clean_nx_class
                logger.debug("Adding class %s to %s", clean_nx_class, entry_name)

        def collect_fields_and_attrs(name: str, dataset: Union[Group, Dataset]):
            for nx_class in class_map:
                if name.startswith(nx_class):
                    name = name.replace(
                        f"{nx_class}/", f"{class_map[nx_class]}[{nx_class}]/"
                    )

            if isinstance(dataset, Dataset):
                logger.debug("Adding field %s/%s", entry_path, name)
                if isinstance(read_data := dataset[()], bytes):
                    read_data = read_data.decode("utf-8")
                template[f"{entry_path}/{name}"] = read_data

            for attr_name, val in dataset.attrs.items():
                if attr_name == "NX_class":
                    continue
                logger.debug("Adding attribute %s/%s/@%s", entry_path, name, attr_name)
                template[f"{entry_path}/{name}/@{attr_name}"] = val

        entry_path = f"/ENTRY[{entry}]"
        with File(file, "r") as h5file:
            # TODO: Check whether h5py does graph traversal
            # which would ensure visiting groups before their fields.
            # In this case one visititems is enough.
            h5file[f"/{entry}"].visititems(collect_groups)
            h5file[f"/{entry}"].visititems(collect_fields_and_attrs)

        logger.log(DEBUG_TEMPLATE, "Processed template %s", template)
        helpers.validate_data_dict(empty_template, Template(template), nxdl_root)

        logger.info(
            f"The entry `{entry}` in file `{file}` is a valid file"
            f" according to the `{nxdl}` application definition."
        )
