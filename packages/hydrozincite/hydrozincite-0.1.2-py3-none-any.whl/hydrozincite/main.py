#!/usr/bin/env python3

import logging
from pathlib import Path

from rich.console import Console
from rich.table import Table

from . import hook, render, repo
from .config.args import args
from .config.config import conf
from .log import log


def main():
    log.set_log(args.log)
    logging.debug("Run hydrozincite")
    console = Console()
    console.rule("[default bold]Hydrozincite[/default bold]")
    match args.sub:
        case "hook":
            if args.write:
                hook.write()
            else:
                hook.list()
        case "info":
            info()
        case _:
            render.html()
    console.rule("[default bold]Zn₅(CO₃)₂(OH)₆[/default bold]")


def info():
    console = Console()
    repositories = repo.get_all_bare(Path(conf["repositories"]))

    table = Table(
        title="Hydrozincite - Zn₅(CO₃)₂(OH)₆",
        show_header=True,
        row_styles=["none", "dim"],
        caption="%s repo in %s" % (len(repositories), conf["repositories"]),
    )
    table.add_column(
        "Repository", justify="left", style="cyan", header_style="cyan", no_wrap=True
    )
    table.add_column("Name", justify="center", style="green", header_style="green")
    table.add_column(
        "Description", style="yellow", header_style="yellow", justify="center"
    )
    table.add_column("Url", justify="right", style="blue", header_style="blue")

    for r in repositories:
        path = r.path.relative_to(Path(conf["repositories"]))
        table.add_row(path.as_posix(), r.name, r.description, r.url)

    console.print(table)
