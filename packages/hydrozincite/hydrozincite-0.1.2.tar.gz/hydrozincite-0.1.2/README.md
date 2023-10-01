# Hydrozincite - Zn₅(CO₃)₂(OH)₆

A simple static page generator for Git repositories.

## Installation

### PyPI

You can find on [PyPI](https://pypi.org/project/hydrozincite/) and install via your favorite package installer for Python, like [pip](https://pypi.org/project/pip/).

```bash
python3 -m pip install hydrozincite
```

### Source

From source, need [build](https://pypi.org/project/build/) & [pdm-backend](https://pypi.org/project/pdm-backend/) as build dependencies.

```bash
python3 -m build --wheel
```

And install via your favorite package installer.

```
python3 -m pip install dist/*.whl
```

Or directly via [pdm](https://pdm.fming.dev).

```bash
pdm install
```

### Archlinux

On Archlinux, via the PKGBUILD file.

```bash
cd PKGBUILD
makepkg -scri
```

## Usage

You can show help via `hydrozincite --help`.

```bash
# Genereate HTML page
hydrozincite --repositories "<path>" --output "<path>" --clone-url "<url>"
# Show info on your repositories
hydrozincite info
# Show info on repository hooks
hydrozincite hook
# Write hooks on your repositories
hydrozincite hook --write
```

It's possible use a config file from 
`./hydrozincite.toml`, `$XDG_CONFIG_HOME/hydrozincite/config.toml`, `~/.config/hydrozincite/config.toml`, `/etc/hydrozincite/config.toml"` or via `--conf <path>` parameter.

```toml
title = "Awesome git repositories !"
clone_url = "https://git.foo.bar"

[bare]
path = "<path>"

[render]
output = "<path>"
template = "<path>"
theme = "default"
```

## Contributing

* See [CONTRIBUTING.md](https://forge.dotslashplay.it/HS-157/Hydrozincite/-/blob/master/CONTRIBUTING.md)


## License

* [BSD 2-clause "Simplified" License](https://forge.dotslashplay.it/HS-157/Hydrozincite/-/blob/master/LICENSE)

## Mirrors

* [forge.dotslashplay.it](https://forge.dotslashplay.it/HS-157/Hydrozincite) (source)
* [git.lett.re](https://git.lett.re/#Hydrozincite)

# Feedback

I take any constructive feedback to improves the project. You can find my email [here](https://forge.dotslashplay.it/HS-157/Hydrozincite/-/blob/master/CONTRIBUTING.md).
