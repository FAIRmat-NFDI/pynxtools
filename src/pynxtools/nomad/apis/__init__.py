from nomad.config.models.plugins import APIEntryPoint


class MyAPIEntryPoint(APIEntryPoint):
    def load(self):
        from pynxtools.nomad.apis.ontology_service import app

        return app


ontology_service = MyAPIEntryPoint(
    name="ontology_service",
    description="A service to provide ontological information for a given NeXus class.",
    prefix="/ontology_service",
)
