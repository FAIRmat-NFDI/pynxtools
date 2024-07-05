from typing import Dict

# associate parsed NeXus entries to a specific metainfo.domain other than the default dft

NXDEF_TO_METAINFO_DOMAIN: Dict[str, str] = {
    "NXem": "em",
    "NXmpes": "mpes",
    "NXmpes_arpes": "mpes",
    "NXarpes": "mpes",
    "NXxps": "xps",
    "NXopt": "opt",
    "NXellipsometry": "opt",
    "NXoptical_spectroscopy": "opt",
    "NXraman": "opt",
    "NXapm": "apm",
    "NXapm_compositionspace_config": "apm",
    "NXapm_compositionspace_results": "apm",
    "NXapm_paraprobe_transcoder_config": "apm",
    "NXapm_paraprobe_transcoder_results": "apm",
    "NXapm_paraprobe_ranger_config": "apm",
    "NXapm_paraprobe_ranger_results": "apm",
    "NXapm_paraprobe_selector_config": "apm",
    "NXapm_paraprobe_selector_results": "apm",
    "NXapm_paraprobe_surfacer_config": "apm",
    "NXapm_paraprobe_surfacer_results": "apm",
    "NXapm_paraprobe_distancer_config": "apm",
    "NXapm_paraprobe_distancer_results": "apm",
    "NXapm_paraprobe_tessellator_config": "apm",
    "NXapm_paraprobe_tessellator_results": "apm",
    "NXapm_paraprobe_spatstat_config": "apm",
    "NXapm_paraprobe_spatstat_results": "apm",
    "NXapm_paraprobe_nanochem_config": "apm",
    "NXapm_paraprobe_nanochem_results": "apm",
    "NXapm_paraprobe_intersector_config": "apm",
    "NXapm_paraprobe_intersector_results": "apm",
    "NXapm_paraprobe_clusterer_config": "apm",
    "NXapm_paraprobe_clusterer_results": "apm",
    "NXspm": "spm",
    "NXsensor_scan": "spm",
    "NXxrd": "xrd",
    "NXxrd_pan": "xrd",
}

NXDEF_TO_METAINFO_DEFAULT: str = "exp"
