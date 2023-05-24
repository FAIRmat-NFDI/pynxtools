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
"""The constraints defining if a swift display_item is assumed a NxImageAngSpace concept."""

# pylint: disable=no-member,line-too-long

# AngSpace, i.e. AngularSpace is not Reciprocal space, recall the following
# RealSpace unit category for dimension scale axes is (NX_)LENGTH
# AngSpace unit category for dimension scale axes is (NX_)ANGLE
# ReciSpace unit category for dimension scale axis is ONE_OVER_LENGTH (not in NeXus yet...)

# releasing line-too-long restriction to avoid having line breaks in the mapping table
# made the experience that when having a widescreen working with the mapping table
# as single-line instructions is more convenient to read and parsable by human eye

# THIS MAPPING TABLE IS INCOMPLETE !!

NxImageAngSpaceDict = {"IGNORE": {"fun": "load_from", "terms": "type"},
                       "IGNORE": {"fun": "load_from", "terms": "uuid"},
                       "IGNORE": {"fun": "load_from", "terms": "created"},
                       "IGNORE": {"fun": "load_from", "terms": "is_sequence"},
                       "IGNORE": {"fun": "load_from", "terms": "intensity_calibration/offset"},
                       "IGNORE": {"fun": "load_from", "terms": "intensity_calibration/scale"},
                       "IGNORE": {"fun": "load_from", "terms": "intensity_calibration/units"},
                       "IGNORE": {"fun": "load_from", "terms": "dimensional_calibrations"},
                       "IGNORE": {"fun": "load_from", "terms": "timezone"},
                       "IGNORE": {"fun": "load_from", "terms": "timezone_offset"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/autostem/Acquisition:Binning"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/autostem/Acquisition:DarkMode"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/autostem/Acquisition:ExposureTime(s)"},
                       "IGNORE": "s",
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/autostem/Acquisition:GainMode"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/autostem/Acquisition:IsFlipped"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/autostem/Acquisition:ReadOutBottom"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/autostem/Acquisition:ReadoutLeft"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/autostem/Acquisition:ReadoutRight"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/autostem/Acquisition:ReadoutTop"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/autostem/Acquisition:ValueNormalization"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/source"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/timestamp"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/sensor_dimensions_hw"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/sensor_readout_area_tlbr"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/is_flipped_horizontally"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/is_gain_corrected"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/is_dark_subtracted"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/frame_number"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/time_point_ns"},
                       "IGNORE": "ns",
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/integration_count"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/counts_per_electron"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/hardware_source_id"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/hardware_source_name"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/exposure"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/binning"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/signal_type"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/valid_rows"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/frame_index"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/channel_index"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/hardware_source/reference_key"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/instrument/high_tension"},
                       "IGNORE": {"fun": "load_from", "terms": "metadata/instrument/defocus"},
                       "IGNORE": {"fun": "load_from", "terms": "title"},
                       "IGNORE": {"fun": "load_from", "terms": "session_id"},
                       "IGNORE": {"fun": "load_from", "terms": "session"},
                       "IGNORE": {"fun": "load_from", "terms": "category"},
                       "IGNORE": {"fun": "load_from", "terms": "version"},
                       "IGNORE": {"fun": "load_from", "terms": "modified"},
                       "IGNORE": {"fun": "load_from", "terms": "data_shape"},
                       "IGNORE": {"fun": "load_from", "terms": "data_dtype"},
                       "IGNORE": {"fun": "load_from", "terms": "collection_dimension_count"},
                       "IGNORE": {"fun": "load_from", "terms": "datum_dimension_count"},
                       "IGNORE": {"fun": "load_from", "terms": "data_modified"},
                       "IGNORE": {"fun": "load_from", "terms": "__large_format"}}
