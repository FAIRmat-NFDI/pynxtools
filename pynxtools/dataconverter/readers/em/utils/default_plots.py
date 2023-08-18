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
"""Logics and functionality to identify and annotate a default plot NXem."""

import h5py
import numpy as np


class NxEmDefaultPlotResolver():
    """Annotate the default plot in an instance of NXem.

    """
    def __init__(self):
        pass

    def annotate_default_plot(self, template: dict, plot_nxpath: str = "") -> dict:
        """Write path to the default plot from root to plot_nxpath."""
        if plot_nxpath != "":
            print(plot_nxpath)
            tmp = plot_nxpath.split("/")
            print(tmp)
            for idx in np.arange(0, len(tmp)):
                if tmp[idx] != "":
                    if idx != 0:
                        template[f'{"/".join(tmp[0:idx])}/@default'] = tmp[idx]
        return template

    def nxs_mtex_get_nxpath_to_default_plot(self,
                                            entry_id: int = 1,
                                            nxs_mtex_file_name: str = "") -> str:
        """Find a path to a default plot (i.e. NXdata instance) if any."""
        h5r = h5py.File(nxs_mtex_file_name, "r")
        if f"/entry{entry_id}/roi1/ebsd/indexing/roi" in h5r:
            h5r.close()
            return f"/entry{entry_id}/roi1/ebsd/indexing/roi"
        h5r.close()
        return ""

    def parse(self, template: dict, entry_id: int = 1) -> dict:
        """Pass because for *.nxs.mtex all data are already in the copy of the output."""
        return template
