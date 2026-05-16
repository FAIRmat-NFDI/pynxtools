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
"""CLI commands for the NXDL → NOMAD metainfo generator.

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
    "--nx-class",
    "nx_class",
    default=None,
    metavar="NX_CLASS",
    help="Generate one NXDL class (e.g. NXdetector).",
)
@click.option(
    "--all",
    "generate_all",
    is_flag=True,
    default=False,
    help="Generate all base classes in dependency order.",
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
        "Directory to write generated .py files into. "
        "Defaults to pynxtools/nomad/metainfo/base_classes/. "
        "Override when generating into a different package (e.g. nomad-measurements)."
    ),
)
def generate_metainfo(
    nx_class: str | None,
    generate_all: bool,
    dry_run: bool,
    force: bool,
    output_dir: Path | None,
) -> None:
    """Generate Python NOMAD metainfo classes from NXDL definitions.

    Exactly one of --nx-class or --all must be given.

    \b
    Examples:
      pynx nomad generate-metainfo --nx-class NXdetector
      pynx nomad generate-metainfo --all
      pynx nomad generate-metainfo --all --dry-run   # CI check: non-zero exit if files differ
      pynx nomad generate-metainfo --all --force      # unconditional overwrite
      pynx nomad generate-metainfo --all \\
          --output-dir ../nomad-measurements/src/nomad_measurements/nexus/metainfo/base_classes
    """
    if not nx_class and not generate_all:
        raise click.UsageError("Specify --nx-class NX_CLASS or --all.")
    if nx_class and generate_all:
        raise click.UsageError("--nx-class and --all are mutually exclusive.")

    from pynxtools.nomad.converters.nxdl_to_metainfo import (
        generate_all_base_classes,
        write_base_class,
    )

    if nx_class:
        try:
            changed = write_base_class(
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
            status = "written" if changed else "unchanged"
            click.echo(f"{nx_class}: {status}")
    else:
        n_changed = generate_all_base_classes(
            dry_run=dry_run, force=force, output_dir=output_dir
        )
        if dry_run:
            if n_changed:
                click.echo(f"{n_changed} file(s) would change.")
                sys.exit(1)
            else:
                click.echo("All files up to date.")
        else:
            click.echo(f"{n_changed} file(s) written.")
