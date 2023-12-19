"""This is config file that mainly maps nexus definition to data path in raw file."""

# pylint: disable=C0301
xrdml = {
    "/ENTRY[entry]/2theta_plot/chi": {
        "xrdml_1.5": {"value": "", "@units": "", "@chi_indices": 0},
    },
    "/ENTRY[entry]/2theta_plot/intensity": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/intensities",
            "@units": "counts/s",
        }
    },
    "/ENTRY[entry]/2theta_plot/omega": {
        "xrdml_1.5": {"value": "", "@units": "", "@omega_indices": 1},
    },
    "/ENTRY[entry]/2theta_plot/title": "Intensity Vs. Two Theta (deg.)",
    "/ENTRY[entry]/2theta_plot/phi": {
        "xrdml_1.5": {"value": "", "@units": "", "@phi_indices": 0},
    },
    "/ENTRY[entry]/2theta_plot/two_theta": {
        "xrdml_1.5": {"value": "", "@units": "deg", "@two_theta_indices": 0},
    },
    "/ENTRY[entry]/COLLECTION[collection]/beam_attenuation_factors": {
        "xrdml_1.5": {"value": "/beamAttenuationFactors", "@units": ""},
    },
    "/ENTRY[entry]/COLLECTION[collection]/omega/start": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/positions_2/startPosition",
            "@units": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/positions_2/unit",
        },
    },
    "/ENTRY[entry]/COLLECTION[collection]/omega/end": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/positions_2/endPosition",
            "@units": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/positions_2/unit",
        },
    },
    "/ENTRY[entry]/COLLECTION[collection]/omega/step": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/comment/entry_2/MinimumstepsizeOmega",
            "@units": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/positions_2/unit",
        },
    },
    "/ENTRY[entry]/COLLECTION[collection]/2theta/start": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/positions_1/startPosition",
            "@units": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/positions_1/unit",
        },
    },
    "/ENTRY[entry]/COLLECTION[collection]/2theta/end": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/positions_1/endPosition",
            "@units": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/positions_1/unit",
        },
    },
    "/ENTRY[entry]/COLLECTION[collection]/2theta/step": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/comment/entry_2/Minimumstepsize2Theta",
            "@units": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/positions_1/unit",
        },
    },
    "/ENTRY[entry]/COLLECTION[collection]/count_time": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/commonCountingTime",
            "@units": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/commonCountingTime/unit",
        },
    },
    "/ENTRY[entry]/COLLECTION[collection]/data_file": {"xrdml_1.5": {"value": ""}},
    "/ENTRY[entry]/COLLECTION[collection]/goniometer_x": {
        "xrdml_1.5": {"value": "/X", "@units": ""},
    },
    "/ENTRY[entry]/COLLECTION[collection]/goniometer_y": {
        "xrdml_1.5": {"value": "/Y", "@units": ""},
    },
    "/ENTRY[entry]/COLLECTION[collection]/goniometer_z": {
        "xrdml_1.5": {"value": "/Z", "@units": ""},
    },
    "/ENTRY[entry]/COLLECTION[collection]/measurement_type": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/measurementType",
            "@units": "",
        },
    },
    "/ENTRY[entry]/INSTRUMENT[instrument]/DETECTOR[detector]/integration_time": {
        "xrdml_1.5": {"value": "", "@units": ""},
    },
    "/ENTRY[entry]/INSTRUMENT[instrument]/DETECTOR[detector]/integration_time/@units": {
        "xrdml_1.5": {"value": "", "@units": ""},
    },
    "/ENTRY[entry]/INSTRUMENT[instrument]/DETECTOR[detector]/scan_axis": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/scan/scanAxis",
            "@units": "",
        },
    },
    "/ENTRY[entry]/INSTRUMENT[instrument]/DETECTOR[detector]/scan_mode": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/scan/mode",
            "@units": "",
        },
    },
    "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/k_alpha_one": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/usedWavelength/kAlpha1",
            "@units": "/xrdMeasurements/xrdMeasurement/usedWavelength/kAlpha1/unit",
        },
    },
    "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/k_alpha_two": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/usedWavelength/kAlpha2",
            "@units": "/xrdMeasurements/xrdMeasurement/usedWavelength/kAlpha2/unit",
        },
    },
    "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/kbeta": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/usedWavelength/kBeta",
            "@units": "/xrdMeasurements/xrdMeasurement/usedWavelength/kBeta/unit",
        },
    },
    "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/ratio_k_alphatwo_k_alphaone": {
        "xrdml_1.5": {"value": "", "@units": ""}
    },
    "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/xray_tube_current": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/incidentBeamPath/xRayTube/current",
            "@units": "/xrdMeasurements/xrdMeasurement/incidentBeamPath/xRayTube/current/unit",
        }
    },
    "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/source_peak_wavelength": {
        "xrdml_1.5": {"value": "", "@units": ""}
    },
    "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/xray_tube_material": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/incidentBeamPath/xRayTube/anodeMaterial",
            "@units": "",
        },
    },
    "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/xray_tube_voltage": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/incidentBeamPath/xRayTube/tension",
            "@units": "/xrdMeasurements/xrdMeasurement/incidentBeamPath/xRayTube/tension/unit",
        }
    },
    "/ENTRY[entry]/SAMPLE[sample]/prepared_by": {"xrdml_1.5": {"value": ""}},
    "/ENTRY[entry]/SAMPLE[sample]/sample_id": {
        "xrdml_1.5": {"value": ""},
    },
    "/ENTRY[entry]/SAMPLE[sample]/sample_mode": {
        "xrdml_1.5": {"value": ""},
    },
    "/ENTRY[entry]/SAMPLE[sample]/sample_name": {
        "xrdml_1.5": {"value": ""},
    },
    "/ENTRY[entry]/definition": "NXxrd_pan",
    "/ENTRY[entry]/method": "X-Ray Diffraction (XRD)",
    "/ENTRY[entry]/q_plot/intensity": {
        "xrdml_1.5": {
            "value": "/xrdMeasurements/xrdMeasurement/scan/dataPoints/intensities",
            "@units": "counts/s",
        },
    },
    "/ENTRY[entry]/q_plot/q": {
        "xrdml_1.5": {"value": "", "@units": ""},
    },
    "/@default": "entry",
    "/ENTRY[entry]/@default": "2theta_plot",
}
