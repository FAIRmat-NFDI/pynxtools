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

import logging
import os

os.environ["OWLREADY2_JAVA_LOG_LEVEL"] = "WARNING"

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from nomad.config import config

from pynxtools.nomad.apis.ontology import (
    ensure_ontology_file,
    fetch_superclasses,
    load_ontology,
)

logger = logging.getLogger("pynxtools")

ontology_service_entry_point = config.get_plugin_entry_point(
    "pynxtools.nomad.apis:ontology_service"
)

# ------------------------------------------------------------------
# FastAPI app and public functions #
# ------------------------------------------------------------------

app = FastAPI(
    root_path=f"{config.services.api_base_path}/ontology_service",
    title="Ontology Service",
    description="A service to provide ontological information for a given NeXus class.",
)


# ------------------------------------------------------------------
# Application routes
# ------------------------------------------------------------------


@app.on_event("startup")
def startup_event():
    """
    Ensure the ontology file is present during application startup.
    if not, generate it.
    """
    try:
        ensure_ontology_file(ontology_service_entry_point.imports)
    except Exception as e:
        logger.error(f"Error during startup: {e}")


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


@app.get("/superclasses/{class_name}")
def get_superclasses_route(class_name: str):
    try:
        ontology = load_ontology(ontology_service_entry_point.imports)
        superclasses = fetch_superclasses(ontology, class_name)
        # return {"superclasses": [str(cls) for cls in superclasses]}
        return {"superclasses": superclasses}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred.")
