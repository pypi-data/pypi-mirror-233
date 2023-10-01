from functools import reduce

from ..config.args import args
from ..config.toml import toml


def deep_get(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


def get_value(value, ref=None, default=None):
    if ref is None:
        ref = [toml, args]
    p = ref.pop()
    r = vars(p) if not isinstance(p, dict) else p
    v = deep_get(r, value.pop())
    if v:
        return v
    elif v is None and ref:
        return get_value(value, ref, default)
    else:
        return default


conf = {
    "title": get_value(["title", "title"]),
    "clone_url": get_value(["clone_url", "clone_url"]),
    "output": get_value(["render.output", "output"]),
    "repositories": get_value(["bare.path", "repositories"]),
    "template": get_value(["render.template", ""]),
    "theme": get_value(["render.theme", "theme"], default="default"),
}
