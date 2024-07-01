from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class PynxtoolsEntryPoint(ParserEntryPoint):
    def load(self):
        from pynxtools.nexus.nexus import HandleNexus

        return HandleNexus(**self.dict())


nexusparser = PynxtoolsEntryPoint(
    name="pynxtools parser",
    description="A parser for nexus files.",
    mainfile_name_re=r".*\.nxs",
)
