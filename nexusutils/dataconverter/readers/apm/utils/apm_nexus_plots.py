#
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
#
"""Generator for NXapm default plots."""

# pylint: disable=E1101

import numpy as np

from nexusutils.dataconverter.readers.shared.shared_utils \
    import get_repo_last_commit


def create_default_plot_reconstruction(template: dict, entry_id: int) -> dict:
    """Compute on-the-fly, add, and give path to discretized reconstruction."""
    trg = "/ENTRY[entry" + str(entry_id) + "]/atom_probe/reconstruction"
    xyz = template[trg + "/reconstructed_positions"]["compress"]

    print("--> Enter histogram computation ")
    print(np.shape(xyz))

    resolution = 1.0  # in nm
    bounds = np.zeros([3, 2], np.float32)  # in nm
    for i in np.arange(0, 3):
        bounds[i, 0] = np.min(xyz[:, i])
        bounds[i, 1] = np.max(xyz[:, i])
    # make the bounding box a quadric prism
    imi = np.floor(bounds[0, 0])
    imx = np.ceil(bounds[0, 1])
    xedges = np.linspace(imi, imx, num=int(np.ceil((imx - imi) / resolution)) + 1,
                         endpoint=True)
    imi = np.floor(bounds[1, 0])
    imx = np.ceil(bounds[1, 1])
    yedges = np.linspace(imi, imx, num=int(np.ceil((imx - imi) / resolution)) + 1,
                         endpoint=True)
    imi = np.floor(bounds[2, 0])
    imx = np.ceil(bounds[2, 1])
    zedges = np.linspace(imi, imx,
                         num=int(np.ceil((imx - imi) / resolution)) + 1,
                         endpoint=True)

    hist3d = np.histogramdd((xyz[:, 0], xyz[:, 1], xyz[:, 2]),
                            bins=(xedges, yedges, zedges))
    del xyz
    assert isinstance(hist3d[0], np.ndarray), \
        "Hist3d computation from the reconstruction failed!"
    assert len(np.shape(hist3d[0])) == 3, \
        "Hist3d computation from the reconstruction failed!"
    for i in np.arange(0, 3):
        assert np.shape(hist3d[0])[i] > 0, \
            "Dimensions " + str(i) + " has no length!"

    trg = "/ENTRY[entry" + str(entry_id) + "]/atom_probe/reconstruction/"
    trg += "naive_point_cloud_density_map/"
    template[trg + "program"] \
        = "nomad-parser-nexus/apm/reader.py"
    template[trg + "program/@version"] \
        = get_repo_last_commit()

    trg += "DATA[data]/"
    template[trg + "title"] = "Discretized reconstruction space"
    # template[trg + "@long_name"] = "Discrete recon space"
    template[trg + "@signal"] = "data_counts"
    template[trg + "@axes"] = ["axis_x", "axis_y", "axis_z"]
    template[trg + "@AXISNAME_indices[axis_x]"] = 0
    template[trg + "@AXISNAME_indices[axis_y]"] = 1
    template[trg + "@AXISNAME_indices[axis_z]"] = 2

    # mind that histogram does not follow Cartesian conventions so a transpose
    # might be necessary, for now we implement the transpose in the appdef
    template[trg + "DATA[data_counts]"] \
        = {"compress": np.array(hist3d[0], np.uint32), "strength": 1}
    template[trg + "DATA[data_counts]/@units"] = ""
    template[trg + "AXISNAME[axis_x]"] \
        = {"compress": np.array(hist3d[1][0][1::], np.float32), "strength": 1}
    template[trg + "AXISNAME[axis_x]/@units"] = "nm"
    template[trg + "AXISNAME[axis_x]/@long_name"] = "x (nm)"
    template[trg + "AXISNAME[axis_y]"] \
        = {"compress": np.array(hist3d[1][1][1::], np.float32), "strength": 1}
    template[trg + "AXISNAME[axis_y]/@units"] = "nm"
    template[trg + "AXISNAME[axis_y]/@long_name"] = "y (nm)"
    template[trg + "AXISNAME[axis_z]"] \
        = {"compress": np.array(hist3d[1][2][1::], np.float32), "strength": 1}
    template[trg + "AXISNAME[axis_z]/@units"] = "nm"
    template[trg + "AXISNAME[axis_z]/@long_name"] = "z (nm)"
    print("Default plot 3D discretized reconstruction at 1nm binning.")
    del hist3d

    return template


def create_default_plot_mass_spectrum(template: dict, entry_id: int) -> dict:
    """Compute on-the-fly, add, and give path to discretized reconstruction."""
    trg = "/ENTRY[entry" + str(entry_id) + "]/atom_probe/mass_to_charge_conversion/"
    m_z = template[trg + "mass_to_charge"]["compress"]

    print("--> Enter mass spectrum computation ")
    print(np.shape(m_z))

    mqmin = 0.0  # in Da, do not plot unphysical values < 0.0
    mqmax = np.ceil(np.max(m_z[:]))
    mqincr = 0.01  # in Da by default

    hist1d = np.histogram(
        m_z[:],
        np.linspace(mqmin, mqmax,
                    num=int(np.ceil((mqmax - mqmin) / mqincr)) + 1,
                    endpoint=True))
    del m_z
    assert isinstance(hist1d[0], np.ndarray), \
        "Hist1d computation from the mass spectrum failed!"
    assert len(np.shape(hist1d[0])) == 1, \
        "Hist1d computation from the mass spectrum failed!"
    for i in np.arange(0, 1):
        assert np.shape(hist1d[0])[i] > 0, \
            "Dimensions " + str(i) + " has no length!"

    trg = "/ENTRY[entry" + str(entry_id) + "]/atom_probe/ranging/"
    trg += "mass_to_charge_distribution/"
    template[trg + "program"] \
        = "nomad-parser-nexus/apm/reader.py"
    template[trg + "program/@version"] \
        = get_repo_last_commit()

    template[trg + "range_increment"] = mqincr
    template[trg + "range_increment/@units"] = "Da"
    template[trg + "range_minmax"] = np.array([mqmin, mqmax], np.float32)
    template[trg + "range_minmax/@units"] = "Da"

    trg += "mass_spectrum/"
    template[trg + "title"] = "Mass spectrum (0.01 Da binning)"
    template[trg + "@signal"] = "data_counts"
    template[trg + "@axes"] = "axis_mass_to_charge"
    template[trg + "@AXISNAME_indices[axis_mass_to_charge]"] = 0
    template[trg + "DATA[data_counts]"] \
        = {"compress": np.array(hist1d[0], np.uint32), "strength": 1}
    template[trg + "DATA[data_counts]/@units"] = ""
    template[trg + "DATA[data_counts]/@long_name"] = "Counts (1)"
    template[trg + "AXISNAME[axis_mass_to_charge]"] \
        = {"compress": np.array(hist1d[1][1::], np.float32), "strength": 1}
    template[trg + "AXISNAME[axis_mass_to_charge]/@units"] = "Da"
    template[trg + "AXISNAME[axis_mass_to_charge]/@long_name"] \
        = "Mass-to-charge-state ratio (Da)"
    print("Plot mass spectrum at 0.01Da binning was created.")
    del hist1d

    return template


def apm_default_plot_generator(template: dict, n_entries: int) -> dict:
    """Copy data from self into template the appdef instance."""
    print("Create default plots on-the-fly...")
    # now the reader implements what is effectively the task of a normalizer step
    # adding plot (discretized representation of the dataset), for now the default plot
    # adding plot mass-to-charge-state ratio histogram,
    # termed mass spectrum in APM community

    # NEW ISSUE: add path to default plottable data

    # check if reconstructed ion positions have been stored
    for entry_id in np.arange(1, n_entries + 1):
        trg = "/ENTRY[entry" + str(entry_id) + "]/atom_probe/mass_to_charge_conversion/"
        has_valid_m_z = False
        path = trg + "mass_to_charge"
        if isinstance(template[trg + "mass_to_charge"], dict):
            if "compress" in template[path].keys():
                if isinstance(template[path]["compress"], np.ndarray):
                    has_valid_m_z = True

        trg = "/ENTRY[entry" + str(entry_id) + "]/atom_probe/reconstruction/"
        has_valid_xyz = False
        path = trg + "reconstructed_positions"
        if isinstance(template[path], dict):
            if "compress" in template[path].keys():
                if isinstance(template[path]["compress"], np.ndarray):
                    has_valid_xyz = True

        has_default_data = has_valid_m_z or has_valid_xyz
        assert has_default_data is True, \
            "Having no recon or mass-to-charge data is inacceptable at the moment!"

        # NEW ISSUE: fall-back solution to plot something else, however
        # currently POS, EPOS and APT provide always xyz, and m_z data

        # generate default plottable and add path
        trg = "/"
        template[trg + "@default"] = "entry" + str(entry_id)
        trg += "ENTRY[entry" + str(entry_id) + "]/"
        template[trg + "@default"] = "atom_probe"

        if has_valid_m_z is True:
            create_default_plot_mass_spectrum(template, entry_id)
            # mass_spectrum main default...
            trg += "atom_probe/"
            template[trg + "@default"] = "ranging"
            trg += "ranging/"
            template[trg + "@default"] = "mass_to_charge_distribution"
            trg += "mass_to_charge_distribution/"
            template[trg + "@default"] = "mass_spectrum"

        if has_valid_xyz is True:
            # ... discretized naive tomographic reconstruction as fallback...
            create_default_plot_reconstruction(template, entry_id)
            # generate path to the default plottable
            if has_valid_m_z is False:
                trg += "atom_probe/"
                template[trg + "@default"] = "reconstruction"
                trg += "reconstruction/"
                template[trg + "@default"] = "naive_point_cloud_density_map"
                trg += "naive_point_cloud_density_map/"
                template[trg + "@default"] = "data"

    return template
