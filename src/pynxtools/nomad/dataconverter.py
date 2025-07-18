import os
import os.path
import re
from typing import Optional

import numpy as np
import yaml

try:
    from nomad.datamodel.data import ArchiveSection, EntryData
    from nomad.metainfo import MEnum, Package, Quantity
    from nomad.units import ureg
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

from pynxtools.dataconverter import convert as pynxtools_converter
from pynxtools.dataconverter import writer as pynxtools_writer
from pynxtools.dataconverter.template import Template
from pynxtools.definitions.dev_tools.utils.nxdl_utils import (
    get_app_defs_names,  # pylint: disable=import-error
)

m_package = Package(name="nexus_data_converter")


def create_eln_dict(archive):
    def transform(quantity_def, section, value, path):
        if quantity_def.unit:
            Q_ = ureg.Quantity
            val_unit = Q_(value, quantity_def.unit)

            default_display_unit = quantity_def.m_annotations.get(
                "eln", {"defaultDisplayUnit": None}
            ).defaultDisplayUnit
            if default_display_unit:
                val_unit = val_unit.to(default_display_unit)

            return dict(
                value=val_unit.magnitude.tolist()
                if isinstance(val_unit.magnitude, np.ndarray)
                else val_unit.magnitude,
                unit=str(format(val_unit.units, "~")),
            )
        return value

    def exclude(quantity_def, section):
        return quantity_def.name in (
            "reader",
            "nxdl",
            "input_files",
            "output",
            "filter",
            "nexus_view",
        )

    eln_dict = archive.m_to_dict(transform=transform, exclude=exclude)
    del eln_dict["data"]["m_def"]

    return eln_dict


def write_yaml(archive, filename, eln_dict):
    with archive.m_context.raw_file(filename, "w") as eln_file:
        yaml.dump(eln_dict["data"], eln_file, allow_unicode=True)


def populate_nexus_subsection(
    template: "Template",
    app_def: str,
    archive,
    logger,
    output_file_path: Optional[str] = None,
    on_temp_file=False,
    nxs_as_entry=True,
):
    """Populate nexus subsection in nomad from nexus template.

    There are three ways to populate nexus subsection from nexus template.
    1. First it writes a nexus file (.nxs), then the nexus subsectoin will be populated from
        that file.
    2. First it write the data in hdf5 datamodel (in a file in memory), later the nexus
        subsection will be populated from that in-memory file.
    3. (This is not yet done.) It directly poulate the nexus subsection from the template.

    Args:
        template: Nexus template.
        app_def: Name of application def NXxrd_pan.
        archive: AntryArchive section.
        output_file_path: Output file should be a relative path not absolute path.
        logger: nomad logger.
        on_temp_file: Whether data will be written in temporary disk, by default False.
        nxs_as_entry: If the nxs file should be as ann nonmad entry or a general file, by default True.

    Raises:
        Exception: could not trigger processing from NexusParser
        Exception: could not trigger processing from NexusParser
    """
    _, nxdl_f_path = pynxtools_converter.helpers.get_nxdl_root_and_path(app_def)

    # Writing nxs file, parse and populate NeXus subsection:
    if output_file_path:
        archive.data.output = os.path.join(
            archive.m_context.raw_path(), output_file_path
        )
        # remove the nexus file and ensure that NOMAD knows that it is removed
        try:
            os.remove(archive.data.output)
            archive.m_context.process_updated_raw_file(
                archive.data.output, allow_modify=True
            )
        except Exception as e:
            pass
        pynxtools_writer.Writer(
            data=template, nxdl_f_path=nxdl_f_path, output_path=archive.data.output
        ).write()
        try:
            from pynxtools.nomad.parser import NexusParser

            nexus_parser = NexusParser()
            nexus_parser.parse(
                mainfile=archive.data.output,
                archive=archive,
                logger=logger,
            )
            # If a NeXus file written a an entry e.g XRD use case
            if nxs_as_entry:
                try:
                    archive.m_context.process_updated_raw_file(
                        output_file_path, allow_modify=True
                    )
                except Exception as e:
                    logger.error(
                        "could not trigger processing",
                        mainfile=archive.data.output,
                        exc_info=e,
                    )
                    raise e
                else:
                    logger.info("triggered processing", mainfile=archive.data.output)
        except Exception as e:
            logger.error("could not trigger processing", exc_info=e)
            raise e

    # Write in temporary file and populate the NeXus section.
    elif not output_file_path or on_temp_file:
        output_file = "temp_file.nxs"
        output_file = os.path.join(archive.m_context.raw_path(), output_file)
        logger.info(
            "No output NeXus file is found and data is being written temporary file."
        )
        try:
            pynxtools_writer.Writer(
                data=template, nxdl_f_path=nxdl_f_path, output_path=output_file
            ).write()

            from pynxtools.nomad.parser import NexusParser

            nexus_parser = NexusParser()
            nexus_parser.parse(mainfile=output_file, archive=archive, logger=logger)
            # Ensure no local reference with the hdf5file
        except Exception as e:
            logger.error("could not trigger processing", exc_info=e)
            raise e
        finally:
            if os.path.isfile(output_file):
                os.remove(output_file)


class ElnYamlConverter(EntryData):
    output = Quantity(
        type=str,
        description="Output yaml file to save all the data. Default: eln_data.yaml",
        a_eln=dict(component="StringEditQuantity"),
        a_browser=dict(adaptor="RawFileAdaptor"),
        default="eln_data.yaml",
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        eln_dict = create_eln_dict(archive)
        write_yaml(archive, archive.data.output, eln_dict)


class NexusDataConverter(EntryData):
    reader = Quantity(
        type=MEnum(sorted(list(set(pynxtools_converter.get_names_of_all_readers())))),
        description="The reader needed to run the Nexus converter.",
        a_eln=dict(component="AutocompleteEditQuantity"),
    )

    nxdl = Quantity(
        type=MEnum(sorted(list(set(get_app_defs_names())))),
        description="The nxdl needed for running the Nexus converter.",
        a_eln=dict(component="AutocompleteEditQuantity"),
    )

    input_files = Quantity(
        type=str,
        shape=["*"],
        description="Input files needed to run the nexus converter.",
        a_eln=dict(component="FileEditQuantity"),
        a_browser=dict(adaptor="RawFileAdaptor"),
    )

    filter = Quantity(
        type=str,
        description="Filter to select additional input files to be converted to NeXus",
        a_eln=dict(component="StringEditQuantity"),
    )

    output = Quantity(
        type=str,
        description="Output Nexus filename to save all the data. Default: output.nxs",
        a_eln=dict(component="StringEditQuantity"),
        a_browser=dict(adaptor="RawFileAdaptor"),
        default="output.nxs",
    )

    export = Quantity(
        type=bool,
        description="Indicates if conversion to NeXus shall happen automatically when ELN is saved",
        a_eln=dict(component="BoolEditQuantity"),
        default=True,
    )

    nexus_view = Quantity(
        type=ArchiveSection,
        description="Link to the NeXus Entry",
        a_eln=dict(overview=True),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        raw_path = archive.m_context.raw_path()
        eln_dict = create_eln_dict(archive)

        input_file_list = (
            list(archive.data.input_files) if archive.data.input_files else []
        )
        if len(eln_dict["data"]) > 0:
            eln_fname = f"{archive.data.output}_eln_data.yaml"
            write_yaml(archive, eln_fname, eln_dict)
            input_file_list.append(eln_fname)

        if not self.export:
            return

        # collect extra input files
        input_list = [os.path.join(raw_path, file) for file in input_file_list]
        if self.filter:
            try:
                extra_inputs = [
                    f for f in os.listdir(raw_path) if re.match(self.filter, f)
                ]
            except Exception as e:
                logger.error(
                    "could not get file list accordonf to the filter provided",
                    mainfile=archive.data.output,
                    exc_info=e,
                )
                extra_inputs = []
        else:
            extra_inputs = []
        extra_inputs += [""]
        # convert all files
        for extra_input in extra_inputs:
            if len(extra_input) > 0:
                input = input_list + [os.path.join(raw_path, extra_input)]
                output = f"{extra_input.replace('.', '_')}.nxs"
            else:
                input = input_list
                output = archive.data.output
            converter_params = {
                "reader": archive.data.reader,
                "nxdl": re.sub(".nxdl$", "", archive.data.nxdl),
                "input_file": input,
                "output": os.path.join(raw_path, output),
            }
            # remove the nexus file and ensure that NOMAD knows that it is removed
            try:
                os.remove(os.path.join(raw_path, output))
                archive.m_context.process_updated_raw_file(
                    archive.data.output, allow_modify=True
                )
            except Exception as e:
                pass
            # create the new nexus file
            try:
                pynxtools_converter.logger = logger
                pynxtools_converter.helpers.logger = logger
                pynxtools_converter.convert(**converter_params)
            except Exception as e:
                logger.error("could not convert to nxs", mainfile=output, exc_info=e)
                continue
            # parse the new nexus file
            try:
                archive.m_context.process_updated_raw_file(output, allow_modify=True)
            except Exception as e:
                logger.error(
                    "could not trigger processing", mainfile=output, exc_info=e
                )
                continue
            else:
                logger.info("triggered processing", mainfile=output)
            # reference the generated nexus file
            try:
                self.nexus_view = f"../upload/archive/mainfile/{output}#/data"
            except Exception as e:
                logger.error(
                    "could not reference the generate nexus file",
                    mainfile=output,
                    exc_info=e,
                )
                continue


m_package.__init_metainfo__()
