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

NX_VELOX_TO_NX_EM = []

("/ENTRY[entry*]/", "to_iso8601", "Acquisition/AcquisitionStartDatetime/DateTime"),
("/ENTRY[entry*]/", "load_from", "Acquisition/BeamType"),
("/ENTRY[entry*]/", "load_from", "Acquisition/SourceType"),
("/ENTRY[entry*]/", "load_from", "Core/MetadataDefinitionVersion"),
("/ENTRY[entry*]/", "load_from", "Core/MetadataSchemaVersion"),
("/ENTRY[entry*]/", "load_from", ["Detectors/Detector-*/CollectionAngleRange/begin", "Detectors/Detector-*/CollectionAngleRange/end"]),
("/ENTRY[entry*]/", "load_from", "Detectors/Detector-*/DetectorName"),
("/ENTRY[entry*]/", "load_from", "Detectors/Detector-*/DetectorType"),
("/ENTRY[entry*]/", "load_from", "Detectors/Detector-*/Enabled"),
("/ENTRY[entry*]/", "load_from", "Detectors/Detector-*/Inserted"),
("/ENTRY[entry*]/", "load_from", "Instrument/ControlSoftwareVersion"),
("/ENTRY[entry*]/", "load_from", "Instrument/InstrumentId"),
("/ENTRY[entry*]/", "load_from", "Instrument/InstrumentModel"),
("/ENTRY[entry*]/", "load_from", "Instrument/Manufacturer"),
("/ENTRY[entry*]/", "load_from", "Optics/AccelerationVoltage"),
("/ENTRY[entry*]/", "load_from", "Optics/Apertures/Aperture-*/Diameter"),
("/ENTRY[entry*]/", "load_from", "Optics/Apertures/Aperture-*/Enabled"),
("/ENTRY[entry*]/", "load_from", "Optics/Apertures/Aperture-*/Name"),
("/ENTRY[entry*]/", "load_from", "Optics/Apertures/Aperture-*/Type"),
("/ENTRY[entry*]/", "load_from", "Optics/BeamConvergence"),
("/ENTRY[entry*]/", "load_from", "Optics/C1LensIntensity"),
("/ENTRY[entry*]/", "load_from", "Optics/C2LensIntensity"),
("/ENTRY[entry*]/", "load_from", "Optics/CameraLength"),
("/ENTRY[entry*]/", "load_from", "Optics/Defocus"),
("/ENTRY[entry*]/", "load_from", "Optics/DiffractionLensIntensity"),
("/ENTRY[entry*]/", "load_from", "Optics/EFTEMOn"),
("/ENTRY[entry*]/", "load_from", "Optics/ExtractorVoltage"),
("/ENTRY[entry*]/", "load_from", "Optics/Focus"),
("/ENTRY[entry*]/", "load_from", "Optics/FullScanFieldOfView/x"),
("/ENTRY[entry*]/", "load_from", "Optics/FullScanFieldOfView/y"),
("/ENTRY[entry*]/", "load_from", "Optics/GunLensSetting"),
("/ENTRY[entry*]/", "load_from", "Optics/HighMagnificationMode"),
("/ENTRY[entry*]/", "load_from", "Optics/IlluminationMode"),
("/ENTRY[entry*]/", "load_from", "Optics/IntermediateLensIntensity"),
("/ENTRY[entry*]/", "load_from", "Optics/LastMeasuredScreenCurrent"),
("/ENTRY[entry*]/", "load_from", "Optics/MiniCondenserLensIntensity"),
("/ENTRY[entry*]/", "load_from", "Optics/NominalMagnification"),
("/ENTRY[entry*]/", "load_from", "Optics/ObjectiveLensIntensity"),
("/ENTRY[entry*]/", "load_from", "Optics/ObjectiveLensMode"),
("/ENTRY[entry*]/", "load_from", "Optics/OperatingMode"),
("/ENTRY[entry*]/", "load_from", "Optics/ProbeMode"),
("/ENTRY[entry*]/", "load_from", "Optics/Projector1LensIntensity"),
("/ENTRY[entry*]/", "load_from", "Optics/Projector2LensIntensity"),
("/ENTRY[entry*]/", "load_from", "Optics/ProjectorMode"),
("/ENTRY[entry*]/", "load_from", "Optics/SpotIndex"),
("/ENTRY[entry*]/", "load_from", "Optics/StemFocus"),
("/ENTRY[entry*]/", "load_from", "Optics/TemOperatingSubMode"),
("/ENTRY[entry*]/", "load_from", "Sample"),
("/ENTRY[entry*]/", "load_from", "Scan/DwellTime"),
("/ENTRY[entry*]/", "load_from", "Stage/AlphaTilt"),
("/ENTRY[entry*]/", "load_from", "Stage/BetaTilt"),
("/ENTRY[entry*]/", "load_from", ["Stage/Position/x", "Stage/Position/y", "Stage/Position/z"])]
