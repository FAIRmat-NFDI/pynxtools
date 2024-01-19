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
"""Map Velox to NeXus concepts."""

# Velox *.emd
# "Core/MetadataDefinitionVersion": ["7.9"]
# "Core/MetadataSchemaVersion": ["v1/2013/07"]
# all *.emd files from https://ac.archive.fhi.mpg.de/D62142 parsed with
# rosettasciio 0.2, hyperspy 1.7.6
# unique original_metadata keys
# keys with hash instance duplicates removed r"([0-9a-f]{32})"
# keys with detector instance duplicates removed r"(Detector-[0-9]+)"
# keys with aperture instance duplicates removed r"(Aperture-[0-9]+)"
# remaining instance duplicates for BM-Ceta and r"(SuperXG[0-9]{2})" removed manually
# Concept names like Projector1Lens<term> and Projector2Lens<term> mean two different concept instances
# of the same concept Projector*Lens<term> in NeXus this would become lens_em1(NXlens_em) name: projector, and field named <term>

# ("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/em_lab/LENS_EM[lens_em*]/name", "is", "C1"),
# ("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/em_lab/LENS_EM[lens_em*]/value", "load_from", "Optics/C1LensIntensity"),
# ("/ENTRY[entry*]/", "load_from", "Optics/C2LensIntensity")
# this can not work but has to be made explicit with an own function that is Velox MetadataSchema-version and NeXus NXem-schema-version-dependent for the lenses

NX_VELOX_TO_NX_EVENT_DATA_EM = [("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/start_time", "unix_to_iso8601", "Acquisition/AcquisitionStartDatetime/DateTime"),
                                ("/ENTRY[entry*]/measurement/em_lab/EBEAM_COLUMN[ebeam_column]/electron_source/emitter_type", "load_from", "Acquisition/SourceType"),
                                ("/ENTRY[entry*]/measurement/em_lab/EBEAM_COLUMN[ebeam_column]/electron_source/probe", "is", "electron"),
                                ("", "ignore", "Core/MetadataDefinitionVersion"),
                                ("", "ignore", "Core/MetadataSchemaVersion"),
                                ("has to be loaded explicitly as not always equally relevant", "ignore", ["Detectors/Detector-*/CollectionAngleRange/begin", "Detectors/Detector-*/CollectionAngleRange/end"]),
                                ("", "ignore", "Detectors/Detector-*/DetectorName"),
                                ("", "ignore", "Detectors/Detector-*/DetectorType"),
                                ("", "ignore", "Detectors/Detector-*/Enabled"),
                                ("", "ignore", "Detectors/Detector-*/Inserted"),
                                ("/ENTRY[entry*]/measurement/em_lab/control_program/program", "is", "Not reported in original_metadata parsed from Velox EMD using rosettasciio"),
                                ("/ENTRY[entry*]/measurement/em_lab/control_program/program/@version", "load_from", "Instrument/ControlSoftwareVersion"),
                                ("/ENTRY[entry*]/measurement/em_lab/FABRICATION[fabrication]/identifier", "load_from", "Instrument/InstrumentId"),
                                ("/ENTRY[entry*]/measurement/em_lab/FABRICATION[fabrication]/model", "load_from", "Instrument/InstrumentModel"),
                                ("/ENTRY[entry*]/measurement/em_lab/FABRICATION[fabrication]/vendor", "load_from", "Instrument/Manufacturer"),
                                ("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/em_lab/EBEAM_COLUMN[ebeam_column]/electron_source/voltage", "load_from", "Optics/AccelerationVoltage"),
                                ("", "ignore", "Optics/Apertures/Aperture-*/Diameter"),
                                ("", "ignore", "Optics/Apertures/Aperture-*/Enabled"),
                                ("", "ignore", "Optics/Apertures/Aperture-*/Name"),
                                ("", "ignore", "Optics/Apertures/Aperture-*/Type"),
                                ("", "ignore", "Optics/BeamConvergence"),
                                ("", "ignore", "Optics/C1LensIntensity"),
                                ("", "ignore", "Optics/C2LensIntensity"),
                                ("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/em_lab/OPTICAL_SYSTEM_EM[optical_system_em]/camera_length", "load_from", "Optics/CameraLength"),
                                ("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/em_lab/OPTICAL_SYSTEM_EM[optical_system_em]/defocus", "load_from", "Optics/Defocus"),
                                ("", "ignore", "Optics/DiffractionLensIntensity"),
                                ("place in optical_system_em", "ignore", "Optics/EFTEMOn"),
                                ("place in electron_source in event data", "ignore", "Optics/ExtractorVoltage"),
                                ("place in optical_system_em", "ignore", "Optics/Focus"),
                                ("place in optical_system_em", "ignore", "Optics/FullScanFieldOfView/x"),
                                ("place in optical_system_em", "ignore", "Optics/FullScanFieldOfView/y"),
                                ("", "ignore", "Optics/GunLensSetting"),
                                ("place in optical_system_em", "ignore", "Optics/HighMagnificationMode"),
                                ("place in optical_system_em", "ignore", "Optics/IlluminationMode"),
                                ("", "ignore", "Optics/IntermediateLensIntensity"),
                                ("place in optical_system_em", "ignore", "Optics/LastMeasuredScreenCurrent"),
                                ("", "ignore", "Optics/MiniCondenserLensIntensity"),
                                ("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/em_lab/OPTICAL_SYSTEM_EM[optical_system_em]/magnification", "load_from", "Optics/NominalMagnification"),
                                ("", "ignore", "Optics/ObjectiveLensIntensity"),
                                ("", "ignore", "Optics/ObjectiveLensMode"),
                                ("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/em_lab/EBEAM_COLUMN[ebeam_column]/operation_mode", "concatenate", ["Optics/OperatingMode",
                                                                                                                                                                                "Optics/TemOperatingSubMode"]),
                                ("", "ignore", "Optics/Projector1LensIntensity"),
                                ("", "ignore", "Optics/Projector2LensIntensity"),
                                ("", "ignore", "Optics/ProjectorMode"),
                                ("", "ignore", "Optics/SpotIndex"),
                                ("", "ignore", "Optics/StemFocus"),
                                ("", "ignore", "Sample"),
                                ("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/em_lab/SCANBOX_EM[scanbox_em]/dwell_time", "load_from", "Scan/DwellTime"),
                                ("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/design", "load_from", "Stage/HolderType"),
                                ("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/tilt1", "load_from", "Stage/AlphaTilt"),
                                ("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/tilt2", "load_from", "Stage/BetaTilt"),
                                ("/ENTRY[entry*]/measurement/event_data_em_set/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/position", "load_from", ["Stage/Position/x",
                                                                                                                                                                  "Stage/Position/y",
                                                                                                                                                                  "Stage/Position/z"])]
