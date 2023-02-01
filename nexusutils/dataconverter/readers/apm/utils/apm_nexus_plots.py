#!/usr/bin/env python3
"""Generator for NXapm default plots."""

# -*- coding: utf-8 -*-
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

# pylint: disable=E1101

import numpy as np


def create_default_plot_reconstruction(template: dict) -> dict:
    """Compute on-the-fly, add, and give path to discretized reconstruction."""
    trg = "/ENTRY[entry]/atom_probe/reconstruction"
    xyz = template[trg + "/reconstructed_positions"]["compress"]

    print('--> Enter histogram computation ')
    print(np.shape(xyz))

    resolution = 1.0  # in nm
    bounds = np.zeros([3, 2], np.float32)  # in nm
    for i in np.arange(0, 3):
        bounds[i, 0] = np.min(xyz[:, i])
        bounds[i, 1] = np.max(xyz[:, i])
    # make the bounding box a quadric prism
    xymax = np.ceil(np.max(np.array(
        np.fabs(bounds[0:1, 0])[0],
        np.fabs(bounds[0:1, 1])[0])))
    zmin = np.floor(bounds[2, 0])
    zmax = np.ceil(bounds[2, 1])

    xedges = np.linspace(-1.0 * xymax, +1.0 * xymax,
                         num=int(np.ceil(2.0 * xymax / resolution)) + 1,
                         endpoint=True)
    # for debugging correct cuboidal storage order make prism a cuboid
    # yedges = np.linspace(-9 + -1.0 * xymax, +9 + +1.0 * xymax,
    #                      num=int(np.ceil((+9 +xymax - (-xymax -9))
    #                                      / resolution))+1,
    #                      endpoint=True)
    yedges = xedges
    zedges = np.linspace(zmin, zmax,
                         num=int(np.ceil((zmax - zmin) / resolution)) + 1,
                         endpoint=True)

    hist3d = np.histogramdd((xyz[:, 0], xyz[:, 1], xyz[:, 2]),
                            bins=(xedges, yedges, zedges))
    del xyz
    assert isinstance(hist3d[0], np.ndarray), \
        'Hist3d computation from the reconstruction failed!'
    assert len(np.shape(hist3d[0])) == 3, \
        'Hist3d computation from the reconstruction failed!'
    for i in np.arange(0, 3):
        assert np.shape(hist3d[0])[i] > 0, \
            'Dimensions ' + str(i) + ' has no length!'

    trg = "/ENTRY[entry]/atom_probe/reconstruction/"
    trg += "naive_point_cloud_density_map/"
    template[trg + "program"] \
        = "nomad-parser-nexus/apm/reader.py"
    template[trg + "program/@version"] \
        = "add current GitCommit message"  # NEW ISSUE

    trg += "DATA[data]/"
    template[trg + "@signal"] = "counts"
    template[trg + "@axes"] = ["xpos", "ypos", "zpos"]
    # mind that histogram does not follow Cartesian conventions so a transpose
    # might be necessary, for now we implement the transpose in the appdef

    template[trg + "counts"] \
        = {"compress": np.array(hist3d[0], np.uint32), "strength": 9}
    template[trg + "counts/@units"] = ""
    template[trg + "xpos"] \
        = {"compress": np.array(hist3d[1][0][1::], np.float32), "strength": 9}
    template[trg + "xpos/@units"] = "nm"
    template[trg + "@xpos_indices"] = 0  # "my x axis"
    template[trg + "ypos"] \
        = {"compress": np.array(hist3d[1][1][1::], np.float32), "strength": 9}
    template[trg + "ypos/@units"] = "nm"
    template[trg + "@ypos_indices"] = 1  # "my y axis"
    template[trg + "zpos"] \
        = {"compress": np.array(hist3d[1][2][1::], np.float32), "strength": 9}
    template[trg + "zpos/@units"] = "nm"
    template[trg + "@zpos_indices"] = 2  # "my z axis"
    template[trg + "@long_name"] = "hist3d tomographic reconstruction"
    print('Default plot 3D discretized reconstruction at 1nm binning.')
    del hist3d

    return template


def create_default_plot_mass_spectrum(template: dict) -> dict:
    """Compute on-the-fly, add, and give path to discretized reconstruction."""
    trg = "/ENTRY[entry]/atom_probe/mass_to_charge_conversion/"
    m_z = template[trg + "mass_to_charge"]["compress"]

    print('--> Enter mass spectrum computation ')
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
        'Hist1d computation from the mass spectrum failed!'
    assert len(np.shape(hist1d[0])) == 1, \
        'Hist1d computation from the mass spectrum failed!'
    for i in np.arange(0, 1):
        assert np.shape(hist1d[0])[i] > 0, \
            'Dimensions ' + str(i) + ' has no length!'

    trg = "/ENTRY[entry]/atom_probe/ranging/"
    trg += "mass_to_charge_distribution/"
    template[trg + "program"] \
        = "nomad-parser-nexus/apm/reader.py"
    template[trg + "program/@version"] \
        = "Add current GitCommit message"  # NEW ISSUE

    template[trg + "range_increment"] = mqincr
    template[trg + "range_increment/@units"] = "Da"
    template[trg + "range_minmax"] = np.array([mqmin, mqmax], np.float32)
    template[trg + "range_minmax/@units"] = "Da"

    trg += "mass_spectrum/"
    template[trg + "@signal"] = "counts"
    template[trg + "@axes"] = "bin_ends"
    template[trg + "counts"] \
        = {"compress": np.array(hist1d[0], np.uint32), "strength": 9}
    template[trg + "counts/@units"] = ""
    template[trg + "@long_name"] = "hist1d mass-to-charge-state ratios"
    template[trg + "bin_ends"] \
        = {"compress": np.array(hist1d[1][1::], np.float32), "strength": 9}
    template[trg + "bin_ends/@units"] = "Da"
    template[trg + "@bin_ends_indices"] = 0
    print('Plot mass spectrum at 0.01Da binning was created.')
    del hist1d

    return template


def apm_default_plot_generator(template: dict) -> dict:
    """Copy data from self into template the appdef instance."""
    print('Create default plots on-the-fly...')
    # now the reader implements what is effectively the task of a normalizer step
    # adding plot (discretized representation of the dataset), for now the default plot
    # adding plot mass-to-charge-state ratio histogram, termed mass spectrum in APM community

    # NEW ISSUE: add path to default plottable data

    # check if reconstructed ion positions have been stored
    trg = "/ENTRY[entry]/atom_probe/reconstruction/"
    has_valid_xyz = False
    path = trg + "reconstructed_positions"
    if isinstance(template[path], dict):
        if "compress" in template[path].keys():
            if isinstance(template[path]["compress"], np.ndarray):
                has_valid_xyz = True

    trg = "/ENTRY[entry]/atom_probe/mass_to_charge_conversion/"
    has_valid_m_z = False
    path = trg + "mass_to_charge"
    if isinstance(template[trg + "mass_to_charge"], dict):
        if "compress" in template[path].keys():
            if isinstance(template[path]["compress"], np.ndarray):
                has_valid_m_z = True

    has_default_data = has_valid_xyz | has_valid_m_z
    assert has_default_data is True, \
        'Having no recon or mass-to-charge data is inacceptable at the moment!'

    # NEW ISSUE: fall-back solution to plot something else, however
    # currently POS, EPOS and APT provide always xyz, and m_z data

    # generate default plottable and add path
    template["/@default"] = "entry"
    template["/ENTRY[entry]/@default"] = "atom_probe"

    if has_valid_xyz is True:
        create_default_plot_reconstruction(template)
        # generate path to the default plottable
        trg = "/ENTRY[entry]/atom_probe/"
        template[trg + "@default"] = "reconstruction"
        trg += "reconstruction/"
        template[trg + "@default"] = "naive_point_cloud_density_map"
        trg += "naive_point_cloud_density_map/"
        template[trg + "@default"] = "data"
        # to instruct h5web of which class this is

    if has_valid_m_z is True:
        create_default_plot_mass_spectrum(template)
        # tomographic reconstruction is the default plot unless...
        if has_valid_xyz is False:
            # ... the mass_spectrum has to take this role
            trg = "/ENTRY[entry]/atom_probe/"
            template[trg + "@default"] = "ranging"
            trg += "ranging/"
            template[trg + "@default"] = "mass_to_charge_distribution"
            trg += "mass_to_charge_distribution/"
            template[trg + "@default"] = "mass_spectrum"

    return template
