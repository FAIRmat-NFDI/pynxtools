# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for the provenance-tracked regeneration of generated metainfo files.

The generator records, per module and class, which members and imports it owns
(a sidecar ``generated_manifest.json``). On regeneration the merge uses that
manifest to keep three cases apart, so hand edits survive a regeneration:

  1. untouched generated member  -> replaced by the fresh template
  2. hand-modified generated member (owned, body changed) -> preserved
  3. hand-added member/import (not owned) -> preserved

For obsolete generated members the template no longer emits, a tier policy
applies: ``contributed`` definitions always drop them; accepted NIAC standards
keep them unless ``--fix`` is passed. Provenance is seeded once, explicitly, by
``bootstrap_manifest`` (run by hand); the merge never guesses.

These tests drive the pure merge/splice functions directly with small synthetic
source strings, so they need no NXDL, no schema build, and run fast.
"""

import ast
import textwrap

import pynxtools.nomad.converters.nxdl_to_metainfo as gen


def _src(body: str) -> str:
    return textwrap.dedent(body).lstrip("\n")


def _manifest_entry(source: str) -> dict:
    """The manifest entry the generator would record for ``source`` (what it owns)."""
    return {
        "classes": gen._class_fingerprints(source),
        "imports": sorted(gen._module_import_texts(source).keys()),
    }


# Previous generator output; also the recorded manifest baseline.
GEN_V1 = _src(
    '''
    from nomad.metainfo import Quantity, Section


    class Foo:
        """Foo."""

        m_def = Section()
        alpha = Quantity(type=str, description="alpha v1")
        beta = Quantity(type=int, description="beta")

        def normalize(self, archive, logger):
            super().normalize(archive, logger)
    '''
)

# Fresh template: alpha changed, beta dropped, gamma added, typical normalize.
GEN_V2 = _src(
    '''
    from nomad.metainfo import Quantity, Section


    class Foo:
        """Foo."""

        m_def = Section()
        alpha = Quantity(type=str, description="alpha v2")
        gamma = Quantity(type=bool, description="gamma")

        def normalize(self, archive, logger):
            super().normalize(archive, logger)
    '''
)

# On disk: GEN_V1 plus a hand-added Quantity and a hand-modified normalize.
EXISTING_WITH_HAND_EDITS = _src(
    '''
    from nomad.metainfo import Quantity, Section


    class Foo:
        """Foo."""

        m_def = Section()
        alpha = Quantity(type=str, description="alpha v1")
        beta = Quantity(type=int, description="beta")
        hand_added = Quantity(type=str, description="hand-added")

        def normalize(self, archive, logger):
            super().normalize(archive, logger)
            self.beta = 1
    '''
)


# ---------------------------------------------------------------------------
# fingerprint + extraction
# ---------------------------------------------------------------------------


def test_member_fingerprint_ignores_whitespace_only_differences():
    one_line = 'alpha = Quantity(type=str, description="x")'
    wrapped = 'alpha = Quantity(type=str,\n        description="x")'  # same tokens
    changed = 'alpha = Quantity(type=int, description="x")'  # real change
    assert gen._member_fingerprint(one_line) == gen._member_fingerprint(wrapped)
    assert gen._member_fingerprint(one_line) != gen._member_fingerprint(changed)


def test_class_fingerprints_and_imports_extracted():
    fps = gen._class_fingerprints(GEN_V1)
    assert set(fps["Foo"]) == {"m_def", "alpha", "beta", "normalize"}
    imports = gen._module_import_texts(GEN_V1)
    assert any("from nomad.metainfo import" in t for t in imports.values())


# ---------------------------------------------------------------------------
# no manifest yet (conservative fallback)
# ---------------------------------------------------------------------------


def test_empty_manifest_preserves_everything_and_removes_nothing():
    """Without provenance the merge cannot classify members, so it keeps them all.

    Provenance is generated once, deterministically, by ``bootstrap_manifest`` (run by
    hand on the already-generated tree); the merge never guesses. Until then it
    behaves conservatively: no member is treated as owned, so nothing is dropped
    and no hand edit is lost.
    """
    merged, new_entry, report = gen._merge_with_provenance(
        EXISTING_WITH_HAND_EDITS, GEN_V2, {}, tier="contributed", fix=True
    )
    ast.parse(merged)
    # every existing member is kept, including the one the template drops (beta)
    assert "beta = Quantity" in merged
    assert "hand_added = Quantity" in merged
    assert "self.beta = 1" in merged
    assert not report["removed"]
    # but the recorded manifest still reflects the fresh template (so the next run,
    # now with provenance, behaves correctly)
    assert set(new_entry["classes"]["Foo"]) == {"m_def", "alpha", "gamma", "normalize"}


# ---------------------------------------------------------------------------
# merge: the three cases + tier policy
# ---------------------------------------------------------------------------


def test_merge_regenerates_untouched_member_and_preserves_hand_content():
    manifest = _manifest_entry(GEN_V1)
    merged, new_entry, report = gen._merge_with_provenance(
        EXISTING_WITH_HAND_EDITS, GEN_V2, manifest, tier="contributed", fix=False
    )
    ast.parse(merged)  # must be valid Python

    # untouched generated member alpha -> regenerated to v2
    assert 'description="alpha v2"' in merged
    # obsolete generated member beta (owned, gone from template) -> removed (contributed)
    assert "beta = Quantity" not in merged
    # brand-new template member gamma -> present
    assert "gamma = Quantity" in merged
    # hand-added helper -> preserved
    assert "hand_added = Quantity" in merged
    # hand-modified normalize -> preserved (keeps the hand body)
    assert "self.beta = 1" in merged

    # new manifest reflects the fresh template's members, not the hand edits
    assert set(new_entry["classes"]["Foo"]) == {"m_def", "alpha", "gamma", "normalize"}
    assert "Foo.hand_added" in report["preserved_added"]
    assert "Foo.normalize" in report["preserved_modified"]
    assert "Foo.beta" in report["removed"]


def test_obsolete_member_tier_policy():
    manifest = _manifest_entry(GEN_V1)
    # template that drops beta; existing == v1 (all generated, unchanged)
    dropped_beta = GEN_V1.replace(
        '    beta = Quantity(type=int, description="beta")\n', ""
    )
    keep, _, _ = gen._merge_with_provenance(
        GEN_V1, dropped_beta, manifest, tier="accepted", fix=False
    )
    drop_fix, _, _ = gen._merge_with_provenance(
        GEN_V1, dropped_beta, manifest, tier="accepted", fix=True
    )
    drop_contrib, _, _ = gen._merge_with_provenance(
        GEN_V1, dropped_beta, manifest, tier="contributed", fix=False
    )
    # accepted tier is add-only without --fix: obsolete generated member kept
    assert "beta = Quantity" in keep
    # a fix pass drops it even from the accepted tier
    assert "beta = Quantity" not in drop_fix
    # contributed always drops it
    assert "beta = Quantity" not in drop_contrib


# ---------------------------------------------------------------------------
# imports
# ---------------------------------------------------------------------------


def test_hand_added_import_preserved_generated_import_refreshed():
    manifest = _manifest_entry(GEN_V1)
    existing = _src(
        """
        from nomad.metainfo import Quantity, Section
        from mypkg.helpers import custom_thing


        class Foo:
            m_def = Section()
            alpha = Quantity(type=str, description="alpha v1")
            beta = Quantity(type=int, description="beta")

            def normalize(self, archive, logger):
                super().normalize(archive, logger)
        """
    )
    new = GEN_V1.replace(
        "from nomad.metainfo import Quantity, Section",
        "from nomad.metainfo import MEnum, Quantity, Section",
    )
    merged, _, report = gen._merge_with_provenance(
        existing, new, manifest, tier="contributed", fix=False
    )
    ast.parse(merged)
    # hand-added import preserved
    assert "from mypkg.helpers import custom_thing" in merged
    # fresh generated import set present
    assert "from nomad.metainfo import MEnum, Quantity, Section" in merged
    assert any("custom_thing" in t for t in report["preserved_imports"])


# ---------------------------------------------------------------------------
# splice fidelity: leading comment + placement of hand-added members
# ---------------------------------------------------------------------------


def test_hand_added_member_keeps_leading_comment_and_placement():
    manifest = _manifest_entry(GEN_V1)
    # a hand-added quantity, with an explanatory comment, sitting among the
    # generated quantities (before normalize)
    existing = _src(
        '''
        from nomad.metainfo import Quantity, Section


        class Foo:
            """Foo."""

            m_def = Section()
            alpha = Quantity(type=str, description="alpha v1")
            beta = Quantity(type=int, description="beta")
            # hand-added helper; explains why it exists
            extra = Quantity(type=str, description="hand-added")

            def normalize(self, archive, logger):
                super().normalize(archive, logger)
        '''
    )
    merged, _, report = gen._merge_with_provenance(
        existing, GEN_V1, manifest, tier="contributed", fix=False
    )
    ast.parse(merged)
    # the leading comment travels with the member
    assert "# hand-added helper; explains why it exists" in merged
    assert "extra = Quantity" in merged
    assert "Foo.extra" in report["preserved_added"]
    # placed among the quantities, not after the method
    assert merged.index("extra = Quantity") < merged.index("def normalize")


# ---------------------------------------------------------------------------
# idempotency
# ---------------------------------------------------------------------------


def test_merge_is_idempotent():
    manifest = _manifest_entry(GEN_V1)
    merged1, entry1, _ = gen._merge_with_provenance(
        EXISTING_WITH_HAND_EDITS, GEN_V2, manifest, tier="contributed", fix=False
    )
    # feed the merged output back in with the written manifest and same template
    merged2, entry2, _ = gen._merge_with_provenance(
        merged1, GEN_V2, entry1, tier="contributed", fix=False
    )
    assert entry1 == entry2
    # hand content still there, still no obsolete member, alpha still v2
    assert "hand_added = Quantity" in merged2
    assert "self.beta = 1" in merged2
    assert "beta = Quantity" not in merged2
    assert 'description="alpha v2"' in merged2
