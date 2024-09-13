import importlib
import os

from click.testing import CliRunner

from pynxtools.dataconverter.verify import verify

# TODO: use importlib for absolute path of pynxtools
#
# # module_path = importlib


current_path = os.getcwd()

if __name__ == "__main__":
    # test_file1 = (
    #     current_path + "/tests/data/test_data_for_validator/SiO2onSi.ellips.nxs"
    # )
    # test_file2 = (
    #     current_path + "/tests/data/test_data_for_validator/201805_WSe2_arpes.nxs"
    # )
    # runner = CliRunner()
    # result = runner.invoke(verify, [test_file2])
    # output = result.output
    # print(result.output)

    from pynxtools.dataconverter import helpers
    from pynxtools.dataconverter.template import Template

    nxdl_root = None
    # nxdl_name =  "NXtest_extended"
    nxdl_name = "NXhdf5_validator_2"
    # nxdl_name = "NXspm"
    if nxdl_root is None:
        nxdl_root, _ = helpers.get_nxdl_root_and_path(nxdl=nxdl_name)

    template = Template()
    helpers.generate_template_from_nxdl(nxdl_root, template)

    print(template)
