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
"""Utilities for defining NXcoordinate_system(_set) and NXtransformation instances."""

# pylint: disable=no-member


NxEmConventions = {"/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/OBJECT[rotation_conventions]/axis_angle_convention": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/OBJECT[rotation_conventions]/euler_angle_convention": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/OBJECT[rotation_conventions]/sign_convention": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/OBJECT[rotation_conventions]/rotation_convention": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/OBJECT[rotation_conventions]/rotation_handedness": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[processing_reference_frame]/type": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[processing_reference_frame]/handedness": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[processing_reference_frame]/x_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[processing_reference_frame]/x_alias": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[processing_reference_frame]/y_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[processing_reference_frame]/y_alias": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[processing_reference_frame]/z_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[processing_reference_frame]/z_alias": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[processing_reference_frame]/origin": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[sample_reference_frame]/type": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[sample_reference_frame]/handedness": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[sample_reference_frame]/x_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[sample_reference_frame]/y_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[sample_reference_frame]/z_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[sample_reference_frame]/origin": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[detector_reference_frame1]/type": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[detector_reference_frame1]/handedness": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[detector_reference_frame1]/x_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[detector_reference_frame1]/y_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[detector_reference_frame1]/z_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[detector_reference_frame1]/origin": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[gnomonic_projection_reference_frame]/type": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[gnomonic_projection_reference_frame]/handedness": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[gnomonic_projection_reference_frame]/x_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[gnomonic_projection_reference_frame]/y_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[gnomonic_projection_reference_frame]/z_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/COORDINATE_SYSTEM[gnomonic_projection_reference_frame]/origin": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/OBJECT[pattern_centre]/[pattern_centre]/x_boundary_convention": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/OBJECT[pattern_centre]/[pattern_centre]/x_normalization_direction": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/OBJECT[pattern_centre]/[pattern_centre]/y_boundary_convention": "undefined",
                   "/ENTRY[entry*]/EM_CONVENTIONS[em_conventions]/OBJECT[pattern_centre]/[pattern_centre]/y_normalization_direction": "undefined"}
