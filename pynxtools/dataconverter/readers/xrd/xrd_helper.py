"""XRD helper stuffs."""

# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings
import numpy as np
from pynxtools.dataconverter.helpers import transform_to_intended_dt
from pynxtools.dataconverter.template import Template


class KeyValueNotFoundWaring(Warning):
    """New Wanrning class"""


def get_a_value_or_warn(
    return_value="",
    warning_catagory=KeyValueNotFoundWaring,
    message="Key-value not found.",
    stack_level=2,
):
    """It returns a value that and rase the warning massage."""

    warnings.warn(f"\033[1;31m {message}:\033[0m]", warning_catagory, stack_level)
    return return_value


def check_unit(unit: str):
    """Handle conflicted unit.
    Some units comes with verdor file that do not follow correct format.
    """
    if unit is None:
        return unit
    unit_map = {
        "Angstrom": "\u212B",
    }
    correct_unit = unit_map.get(unit, None)
    if correct_unit is None:
        return unit
    return correct_unit


# pylint: disable=too-many-statements
def feed_xrdml_to_template(template, xrd_dict, eln_dict, file_term, config_dict=None):
    """Fill template with data from xrdml type file.

    Parameters
    ----------
    template : Dict
        Template generated from nxdl definition file.
    xrd_dict : dict
        Just a dict mapping slash separated key to the data. The key is equivalent to the
        path directing the location in data file.
    eln_dict : dict
        That brings the data from user especially using NeXus according to NeXus concept.
    file_term : str
        Terminological string to describe file ext. and version (e.g. xrdml_1.5) to find proper
        dict from config file.
    config_dict : Dict
        Dictionary from config file that maps NeXus concept to data from different data file
        versions. E.g.
        {
         "/ENTRY[entry]/2theta_plot/chi": {"file_exp": {"value": "",
                                                        "@units": ""},},
         "/ENTRY[entry]/2theta_plot/intensity": {"file_exp": {"value": "/detector",
                                                              "@units": ""},}
         }
    """

    def fill_template_from_config_data(
        config_dict: dict, template: Template, xrd_dict: dict, file_term: str
    ) -> None:
        """
        Parameters
        ----------
        config_dict : dict
            Python dict that is nested dict for different file versions.
            e.g.
            {"/ENTRY[entry]/2theta_plot/chi": {"file_exp": {"value": "",
                                                    "@units": ""},},
            "/ENTRY[entry]/2theta_plot/intensity": {"file_exp": {"value": "/detector",
                                                            "@units": ""},}
            }
        template : Template

        Return
        ------
        None
        """
        for nx_key, val in config_dict.items():
            if isinstance(val, dict):
                raw_data_des: dict = val.get(file_term, None)
                if raw_data_des is None:
                    raise ValueError(
                        f"conflict file config file does not have any data map"
                        f" for file {file_term}"
                    )
                # the field does not have any value
                if not raw_data_des.get("value", None):
                    continue
                # Note: path is the data path in raw file
                for val_atr_key, path in raw_data_des.items():
                    # data or field val
                    if val_atr_key == "value":
                        template[nx_key] = xrd_dict.get(path, None)
                    elif path and val_atr_key == "@units":
                        template[nx_key + "/" + val_atr_key] = check_unit(
                            xrd_dict.get(path, None)
                        )
                    # attr e.g. @AXISNAME
                    elif path and val_atr_key.startswith("@"):
                        template[nx_key + "/" + val_atr_key] = xrd_dict.get(path, None)
            if not isinstance(val, dict) and isinstance(val, str):
                template[nx_key] = val

    def two_theta_plot():
        intesity = transform_to_intended_dt(
            template.get("/ENTRY[entry]/2theta_plot/intensity", None)
        )
        if intesity is not None:
            intsity_len = np.shape(intesity)[0]
        else:
            raise ValueError("No intensity is found")

        two_theta_gr = "/ENTRY[entry]/2theta_plot/"
        if template.get(f"{two_theta_gr}omega", None) is None:
            omega_start = template.get(
                "/ENTRY[entry]/COLLECTION[collection]/omega/start", None
            )
            omega_end = template.get(
                "/ENTRY[entry]/COLLECTION[collection]/omega/end", None
            )

            template["/ENTRY[entry]/2theta_plot/omega"] = np.linspace(
                float(omega_start), float(omega_end), intsity_len
            )

        if template.get(f"{two_theta_gr}two_theta", None) is None:
            tw_theta_start = template.get(
                "/ENTRY[entry]/COLLECTION[collection]/2theta/start", None
            )
            tw_theta_end = template.get(
                "/ENTRY[entry]/COLLECTION[collection]/2theta/end", None
            )
            template[f"{two_theta_gr}two_theta"] = np.linspace(
                float(tw_theta_start), float(tw_theta_end), intsity_len
            )
        template[two_theta_gr + "/" + "@axes"] = ["two_theta"]
        template[two_theta_gr + "/" + "@signal"] = "intensity"

    def q_plot():
        q_plot_gr = "/ENTRY[entry]/q_plot"
        alpha_2 = template.get(
            "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/k_alpha_two", None
        )
        alpha_1 = template.get(
            "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/k_alpha_one", None
        )
        two_theta: np.ndarray = template.get(
            "/ENTRY[entry]/2theta_plot/two_theta", None
        )
        if two_theta is None:
            raise ValueError("Two-theta data is not found")
        if isinstance(two_theta, np.ndarray):
            theta: np.ndarray = two_theta / 2
        ratio_k = "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/ratio_k_alphatwo_k_alphaone"
        if alpha_1 and alpha_2:
            ratio = alpha_2 / alpha_1
            template[ratio_k] = ratio
            lamda = ratio * alpha_1 + (1 - ratio) * alpha_2
            q_vec = (4 * np.pi / lamda) * np.sin(np.deg2rad(theta))
            template[q_plot_gr + "/" + "q_vec"] = q_vec
            template[q_plot_gr + "/" + "@q_vec_indicies"] = 0
            template[q_plot_gr + "/" + "@axes"] = ["q_vec"]

        template[q_plot_gr + "/" + "@signal"] = "intensity"

    def handle_special_fields():
        """Some fields need special treatment."""

        key = "/ENTRY[entry]/COLLECTION[collection]/goniometer_x"
        gonio_x = template.get(key, None)

        template[key] = (
            gonio_x[0]
            if (isinstance(gonio_x, np.ndarray) and gonio_x.shape == (1,))
            else gonio_x
        )

        key = "/ENTRY[entry]/COLLECTION[collection]/goniometer_y"
        gonio_y = template.get(key, None)

        template[key] = (
            gonio_y[0]
            if (isinstance(gonio_y, np.ndarray) and gonio_y.shape == (1,))
            else gonio_y
        )

        key = "/ENTRY[entry]/COLLECTION[collection]/goniometer_z"
        gonio_z = template.get(key, None)

        template[key] = (
            gonio_z[0]
            if (isinstance(gonio_z, np.ndarray) and gonio_z.shape == (1,))
            else gonio_z
        )

        key = "/ENTRY[entry]/COLLECTION[collection]/count_time"
        count_time = template.get(key, None)

        template[key] = (
            count_time[0]
            if (isinstance(count_time, np.ndarray) and count_time.shape == (1,))
            else count_time
        )

    fill_template_from_config_data(config_dict, template, xrd_dict, file_term)
    two_theta_plot()
    q_plot()
    handle_special_fields()

    fill_template_from_eln_data(eln_dict, template)


# pylint: disable=unused-argument
def feed_udf_to_template(template, xrd_dict, eln_dict, config_dict):
    """_summary_

    Parameters
    ----------
    template : _type_
        _description_
    xrd_dict : _type_
        _description_
    eln_dict : _type_
        _description_
    config_dict : _type_
        _description_
    """


def feed_raw_to_template(template, xrd_dict, eln_dict, config_dict):
    """_summary_

    Parameters
    ----------
    template : _type_
        _description_
    xrd_dict : _type_
        _description_
    eln_dict : _type_
        _description_
    config_dict : _type_
        _description_
    """


def feed_xye_to_template(template, xrd_dict, eln_dict, config_dict):
    """_summary_

    Parameters
    ----------
    template : _type_
        _description_
    xrd_dict : _type_
        _description_
    eln_dict : _type_
        _description_
    config_dict : _type_
        _description_
    """


def fill_template_from_eln_data(eln_data_dict, template):
    """Fill out the template from dict that generated from eln yaml file.
    Parameters:
    -----------
    eln_data_dict : dict[str, Any]
        Python dictionary from eln file.
    template : dict[str, Any]
    Return:
    -------
    None
    """

    if eln_data_dict is None:
        return
    for e_key, e_val in eln_data_dict.items():
        template[e_key] = transform_to_intended_dt(e_val)


def fill_nxdata_from_xrdml(
    template, xrd_flattend_dict, dt_nevigator_from_config_file, data_group_concept
):
    """_summary_

    Parameters
    ----------
    template : _type_
        _description_
    xrd_flattend_dict : _type_
        _description_
    dt_nevigator_from_config_file : _type_
        _description_
    data_group_concept : _type_
        _description_
    """
