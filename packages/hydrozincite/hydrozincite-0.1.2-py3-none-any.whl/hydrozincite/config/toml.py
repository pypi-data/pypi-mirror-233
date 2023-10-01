import os
import tomllib
from pathlib import Path

from ..config.args import args

XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", ".")

conf_path = [
    Path("./hydrozincite.toml"),
    Path(f"{XDG_CONFIG_HOME}/hydrozincite/config.toml"),
    Path(Path().home() / ".config/hydrozincite/config.toml"),
    Path("/etc/hydrozincite/config.toml"),
]


def get_conf_path():
    for p in conf_path:
        if p.exists():
            return p


def load():
    config_file = Path(args.conf) if args.conf else get_conf_path()
    if config_file:
        with config_file.open("rb") as f:
            conf = tomllib.load(f)
            return conf
    else:
        return {}


toml = load()
