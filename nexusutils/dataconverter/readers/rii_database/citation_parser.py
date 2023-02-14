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
"""Parse references from rii yaml files"""
from dataclasses import dataclass, field
import re
from typing import Any, Dict, Optional
import requests_cache


@dataclass
class Citation:
    """A representation for a citation"""

    _raw_str: str = field(repr=False)
    ref_str: str
    url: Optional[str]
    doi: Optional[str]
    session: Optional[requests_cache.CachedSession] = None
    bibtex: Optional[str] = None

    @staticmethod
    def parse_citations(reference: str, download_bibtex: bool = False):
        """Parses a reference string into its components"""
        cites = re.split(r"<br\s*\/?\s*>", reference)

        clean_cites = []
        for cite in cites:
            clean_cites.append(Citation(cite, download_bibtex))
        return clean_cites

    def __init__(
        self, ref_str: str, download_bibtex: bool = False, desc: Optional[str] = None
    ):
        self._raw_str = ref_str
        self.ref_str = re.sub(
            r"\<\/?[^\<\>]*\>",
            "",
            re.search(r"(?:\d\))?\s*(.*)", ref_str).group(1),
        )
        self.get_non_doi_url()
        self.get_doi()

        if desc:
            self.description = desc
        else:
            self.description = (
                "Literature reference from which this "
                "dispersion function was extracted."
            )

        if download_bibtex:
            self.download_bibtex()

    def download_bibtex(self):
        """Requests the bibtext entry for a given doi"""
        if not self.doi:
            return

        if self.session is None:
            self.session = requests_cache.CachedSession("rii_bibtex")

        req = self.session.get(
            f"https://doi.org/{self.doi}",
            timeout=30,
            headers={"Accept": "application/x-bibtex"},
        )
        if req.status_code == 200:
            self.bibtex = req.text

    def get_non_doi_url(self):
        """Extract urls which are not dois"""
        url = re.search(r"href\=\"([^\"]+)\"", self._raw_str)
        self.url = url.group(1) if url and "doi.org" not in url.group(1) else None

    def get_doi(self):
        """Extracts doi from a reference string"""
        doi_match = re.search(r"\".*doi\.org\/([^\"]+)\"", self._raw_str)
        self.doi = doi_match.group(1) if doi_match else None

    def write_entries(self, template: Dict[str, Any], path: str):
        """Write entries to nexusutils template"""
        reference_identifier = "REFERENCES"
        name = basename = "reference"

        while f"{path}/{reference_identifier}[{name}]/text" in template:
            count = locals().get("count", 0) + 1
            name = f"{basename}{count}"

        base_path = f"{path}/{reference_identifier}[{name}]"
        if self.url:
            template[f"{base_path}/url"] = self.url
        if self.doi:
            template[f"{base_path}/doi"] = self.doi
        if self.bibtex:
            template[f"{base_path}/bibtex"] = self.bibtex

        template[f"{base_path}/text"] = self.ref_str
        template[f"{base_path}/description"] = self.description
