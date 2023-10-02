#!/usr/bin/env python3
from __future__ import annotations

import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict

import click

from toolforge_cli.config import get_loaded_config
from toolforge_weld.config import Config

LOGGER = logging.getLogger("toolforge" if __name__ == "__main__" else __name__)


def _run_external_command(*args, binary: str, verbose: bool = False, debug: bool = False) -> None:
    env = os.environ.copy()
    cmd = [binary, *args]
    env["TOOLFORGE_CLI"] = "1"
    env["TOOLFORGE_VERBOSE"] = "1" if verbose else "0"
    env["TOOLFORGE_DEBUG"] = "1" if debug else "0"

    LOGGER.debug(f"Running command: {cmd}")
    proc = subprocess.Popen(
        args=cmd, bufsize=0, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False, env=env
    )
    returncode = proc.poll()
    while returncode is None:
        time.sleep(0.1)
        returncode = proc.poll()

    if proc.returncode != 0:
        raise subprocess.CalledProcessError(returncode=proc.returncode, output=None, stderr=None, cmd=cmd)


def _add_discovered_subcommands(cli: click.Group, config: Config) -> click.Group:
    bins_path = os.environ.get("PATH", ".")
    subcommands: Dict[str, Path] = {}
    LOGGER.debug("Looking for subcommands...")
    for dir_str in reversed(bins_path.split(":")):
        dir_path = Path(dir_str)
        LOGGER.debug(f"Checking under {dir_path}...")
        for command in dir_path.glob(f"{config.toolforge_prefix}*"):
            LOGGER.debug(f"Checking {command}...")
            if command.is_file() and os.access(command, os.X_OK):
                subcommand_name = command.name[len(config.toolforge_prefix) :]
                subcommands[subcommand_name] = command

    LOGGER.debug(f"Found {len(subcommands)} subcommands.")
    for name, binary in subcommands.items():
        bin_path = str(binary.resolve())

        @cli.command(
            name=name,
            context_settings=dict(
                ignore_unknown_options=True,
            ),
            add_help_option=False,
        )
        @click.argument("args", nargs=-1, type=click.UNPROCESSED)
        @click.pass_context
        def _new_command(ctx, args, bin_path: str = bin_path):  # noqa
            verbose = ctx.obj.get("verbose", False)
            debug = ctx.obj.get("debug", False)
            _run_external_command(*args, verbose=verbose, debug=debug, binary=bin_path)

    return cli


@click.version_option(prog_name="Toolforge CLI")
@click.group(name="toolforge", help="Toolforge command line")
@click.option(
    "-v",
    "--verbose",
    help="Show extra verbose output. NOTE: Do no rely on the format of the verbose output",
    is_flag=True,
)
@click.option(
    "-d",
    "--debug",
    help="show logs to debug the toolforge-* packages. For extra verbose output for say build or job, see --verbose",
    is_flag=True,
)
@click.pass_context
def toolforge(ctx: click.Context, verbose: bool, debug: bool) -> None:
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["debug"] = debug
    pass


@toolforge.command(name="_commands", hidden=True)
def internal_commands():
    """Used internally for tab completion."""
    for name, command in sorted(toolforge.commands.items()):
        if command.hidden:
            continue
        click.echo(name)


def main() -> int:
    # this is needed to setup the logging before the subcommand discovery
    res = toolforge.parse_args(ctx=click.Context(command=toolforge), args=sys.argv)
    if "-d" in res or "--debug" in res:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    config = get_loaded_config()
    _add_discovered_subcommands(cli=toolforge, config=config)
    try:
        toolforge()
    except subprocess.CalledProcessError as err:
        return err.returncode

    return 0


if __name__ == "__main__":
    main()
