import logging
import os
from datetime import datetime
from distutils.dir_util import copy_tree
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from rich.console import Console

from . import repo
from .config.config import conf

XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", ".")

templates_path = [
    Path("./templates"),
    Path(f"{XDG_CONFIG_HOME}/hydrozincite/templates"),
    Path(Path().home() / ".config/hydrozincite/templates"),
    Path("/usr/share/hydrozincite/templates"),
]


def get_templates_path():
    for p in templates_path:
        if p.exists():
            return p


def html():
    console = Console()

    logging.debug("Find all git bare repositories")
    repositories = repo.get_all_bare(Path(conf["repositories"]))

    template_dir = Path(conf["template"]) if conf["template"] else get_templates_path()
    template = template_dir / conf["theme"]
    static = template / "static"
    output = Path(conf["output"])

    title = conf["title"]
    now = datetime.now()
    clone_url = conf["clone_url"]

    logging.debug("Template directory : %s", template.as_posix())
    file_loader = FileSystemLoader(template.as_posix())
    env = Environment(loader=file_loader)
    tplt = env.get_template("index.html.j2")

    logging.debug("Generate HTML")
    render = tplt.render(
        now=now,
        repositories=repositories,
        title=title,
        clone_url=clone_url,
    )

    if not output.exists() and not output.is_dir():
        output.mkdir()

    index = output / "index.html"
    with open(index, "w") as fh:
        logging.debug("Write index.html file : %s" % index.absolute())
        fh.write(render)

    if static.exists():
        logging.debug("Copy static directory from %s" % static.absolute())
        static_output = output / "static"
        copy_tree(static.as_posix(), static_output.as_posix())

    console.print("HTML generated")
