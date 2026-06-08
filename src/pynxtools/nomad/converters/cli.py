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
"""
CLI commands for the NXDL → NOMAD metainfo generator.

Exposes one symbol consumed by the ``pynx nomad `` group:

``generate-metainfo``
    Click command for creating the NeXus NOMAD metainfo as Python classes.
"""

from __future__ import annotations

import sys
from pathlib import Path

import click


@click.command("generate-metainfo")
@click.option(
    "--nxdl",
    "nx_class",
    default=None,
    metavar="NXDL",
    help="Generate one NXDL class (e.g. NXdetector).",
)
@click.option(
    "--all",
    "generate_all",
    is_flag=True,
    default=False,
    help="Generate all categories (applications first, then base classes with --force).",
)
@click.option(
    "--all-base",
    "generate_all_base",
    is_flag=True,
    default=False,
    help="Generate all base-category classes only.",
)
@click.option(
    "--all-applications",
    "generate_all_applications",
    is_flag=True,
    default=False,
    help="Generate all application-category classes only.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Report what would change without writing any files. Exits non-zero if files differ.",
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Overwrite existing files even if no new members were added.",
)
@click.option(
    "--output-dir",
    "output_dir",
    default=None,
    metavar="DIR",
    type=click.Path(file_okay=False, path_type=Path),
    help=(
        "Parent directory for generated .py files; base_classes/ or applications/ "
        "is appended automatically. Omit to write into the pynxtools-internal "
        "nomad/metainfo/ directory. Pass an explicit path when generating into a "
        "different package (e.g. nomad-measurements/src/schema_packages/...)."
    ),
)
def generate_metainfo(
    nx_class: str | None,
    generate_all: bool,
    generate_all_base: bool,
    generate_all_applications: bool,
    dry_run: bool,
    force: bool,
    output_dir: Path | None,
) -> None:
    """Generate Python NOMAD metainfo classes from NXDL definitions.

    Exactly one of --nxdl, --all, --all-base, or --all-applications must be given.

    \b
    Examples:
      pynx nomad generate-metainfo --nxdl NXdetector
      pynx nomad generate-metainfo --all-base
      pynx nomad generate-metainfo --all-applications
      pynx nomad generate-metainfo --all           # apps first, then base --force
      pynx nomad generate-metainfo --all --dry-run  # CI check
      pynx nomad generate-metainfo --all \\
          --output-dir ../nomad-measurements/src/nomad_measurements/nexus/metainfo
    """
    flags = [nx_class, generate_all, generate_all_base, generate_all_applications]
    if sum(bool(f) for f in flags) == 0:
        raise click.UsageError(
            "Specify one of --nxdl NX_CLASS, --all, --all-base, or --all-applications."
        )
    if sum(bool(f) for f in flags) > 1:
        raise click.UsageError(
            "--nxdl, --all, --all-base, and --all-applications are mutually exclusive."
        )

    from pynxtools.nomad.converters.nxdl_to_metainfo import (
        generate_all_applications as _gen_apps,
    )
    from pynxtools.nomad.converters.nxdl_to_metainfo import (
        generate_all_base_classes,
        write_class,
    )

    def _report(n_changed: int) -> None:
        if dry_run:
            if n_changed:
                click.echo(f"{n_changed} file(s) would change.")
                sys.exit(1)
            else:
                click.echo("All files up to date.")
        else:
            click.echo(f"{n_changed} file(s) written.")

    if nx_class:
        try:
            changed = write_class(
                nx_class, dry_run=dry_run, force=force, output_dir=output_dir
            )
        except Exception as exc:
            raise click.ClickException(str(exc)) from exc
        if dry_run:
            if changed:
                click.echo(f"Would update: {nx_class}")
                sys.exit(1)
            else:
                click.echo(f"Up to date: {nx_class}")
        else:
            click.echo(f"{nx_class}: {'written' if changed else 'unchanged'}")

    elif generate_all_base:
        _report(
            generate_all_base_classes(
                dry_run=dry_run, force=force, output_dir=output_dir
            )
        )

    elif generate_all_applications:
        _report(_gen_apps(dry_run=dry_run, force=force, output_dir=output_dir))

    else:  # --all: applications first, then base with --force to pick up cross-category refs
        n = _gen_apps(dry_run=dry_run, force=force, output_dir=output_dir)
        n += generate_all_base_classes(
            dry_run=dry_run, force=True, output_dir=output_dir
        )
        _report(n)
