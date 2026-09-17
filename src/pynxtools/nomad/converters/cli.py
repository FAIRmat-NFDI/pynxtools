# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0
# Full license text: LICENSES/Apache-2.0.txt. See docs/learn/pynxtools/licensing.md
# for why this package mixes Apache-2.0 and LGPL-3.0-or-later licensed files.
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


def _flag_name(ctx: click.Context, param_name: str) -> str:
    """Return the primary ``--option`` string for a parameter name."""
    for param in ctx.command.params:
        if param.name == param_name and param.opts:
            return param.opts[0]
    return "--" + param_name.replace("_", "-")


class MutuallyExclusiveOption(click.Option):
    """A click option that refuses to be combined with the options it lists.

    The exclusion must be declared on the options themselves via
    ``cls=MutuallyExclusiveOption, mutually_exclusive=[<other-option>]``.
    """

    def __init__(self, *args, **kwargs):
        self.mutually_exclusive: set[str] = set(kwargs.pop("mutually_exclusive", ()))
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if opts.get(self.name):
            conflicts = [name for name in self.mutually_exclusive if opts.get(name)]
            if conflicts:
                others = ", ".join(_flag_name(ctx, name) for name in conflicts)
                raise click.UsageError(
                    f"{_flag_name(ctx, self.name)} cannot be combined with {others}."
                )

        return super().handle_parse_result(ctx, opts, args)


_GENERATION_OPTIONS = {
    "nx_class",
    "generate_all",
    "generate_all_base",
    "generate_all_applications",
}


def _mutually_exclusive_with(*, excluding: str) -> list[str]:
    """Return all other generation options that are mutually exclusive with the given one."""
    return sorted(_GENERATION_OPTIONS - {excluding})


_GENERATION_TARGET_HELP = (
    "Choose exactly one of --nxdl, --all, --all-base, or --all-applications."
)


@click.command("generate-metainfo")
@click.option(
    "--nxdl",
    "nx_class",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=_mutually_exclusive_with(excluding="nx_class"),
    default=None,
    metavar="NXDL",
    help=f"Generate a single NXDL class, e.g. NXdetector. {_GENERATION_TARGET_HELP}",
)
@click.option(
    "--all",
    "generate_all",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=_mutually_exclusive_with(excluding="generate_all"),
    is_flag=True,
    default=False,
    help="Generate all categories (applications first, then base classes). "
    f"{_GENERATION_TARGET_HELP}",
)
@click.option(
    "--all-base",
    "generate_all_base",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=_mutually_exclusive_with(excluding="generate_all_base"),
    is_flag=True,
    default=False,
    help=f"Generate all base classes only. {_GENERATION_TARGET_HELP}",
)
@click.option(
    "--all-applications",
    "generate_all_applications",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=_mutually_exclusive_with(excluding="generate_all_applications"),
    is_flag=True,
    default=False,
    help=f"Generate all application definition classes only. {_GENERATION_TARGET_HELP}",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Report what would change without writing any files, and exit with a "
    "non-zero status if anything would differ.",
)
@click.option(
    "--force",
    "force",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["fix"],
    is_flag=True,
    default=False,
    help="Overwrite existing files, discarding all hand-written content. "
    "Cannot be combined with --fix, since --fix preserves hand content by design.",
)
@click.option(
    "--fix",
    "fix",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["force"],
    is_flag=True,
    default=False,
    help="Fix wrong generator output by also dropping now-obsolete generated "
    "members from the accepted NIAC standards (base_classes/applications), not "
    "only from contributed definitions. Hand-modified and hand-added content is "
    "still preserved. Cannot be combined with --force.",
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
    fix: bool,
    output_dir: Path | None,
) -> None:
    """Generate Python NOMAD metainfo classes from NXDL definitions.

    Choose exactly one target: --nxdl for a single class, --all for everything,
    or --all-base / --all-applications for one category. The remaining options
    modify how that target is generated and can be combined freely, except that
    --force and --fix are mutually exclusive: --force overwrites everything and
    discards hand-written content, while --fix is provenance-aware and preserves
    it while still dropping obsolete generated members.

    \b
    Examples:
      pynx nomad generate-metainfo --nxdl NXdetector
      pynx nomad generate-metainfo --all --dry-run  # CI check
      pynx nomad generate-metainfo --all --fix      # also drop obsolete accepted-tier members
      pynx nomad generate-metainfo --all \\
          --output-dir ../nomad-measurements/src/nomad_measurements/nexus/metainfo
    """
    if not any((nx_class, generate_all, generate_all_base, generate_all_applications)):
        raise click.UsageError(
            "Choose exactly one target: --nxdl NXDL, --all, --all-base, "
            "or --all-applications."
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
                nx_class,
                dry_run=dry_run,
                force=force,
                output_dir=output_dir,
                fix=fix,
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
                dry_run=dry_run,
                force=force,
                output_dir=output_dir,
                fix=fix,
            )
        )

    elif generate_all_applications:
        _report(
            _gen_apps(
                dry_run=dry_run,
                force=force,
                output_dir=output_dir,
                fix=fix,
            )
        )

    else:  # --all: applications first, then base classes.
        n = _gen_apps(dry_run=dry_run, force=force, output_dir=output_dir, fix=fix)
        n += generate_all_base_classes(
            dry_run=dry_run, force=force, output_dir=output_dir, fix=fix
        )
        _report(n)
