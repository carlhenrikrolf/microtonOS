from frozendict import frozendict
from os import path
import tomllib as toml


def make_immutable(obj):
    if isinstance(obj, dict):
        return frozendict({k: make_immutable(v) for k, v in obj.items()})
    elif isinstance(obj, list):
        return tuple(make_immutable(item) for item in obj)  # Use tuple for lists
    else:
        return obj


def load_relative(current_file, relative_path):
    script_path = path.abspath(current_file)
    script_dir = path.dirname(script_path)
    return path.join(script_dir, relative_path)


def load_config(current_file, relative_path, frozen=True):
    config_path = load_relative(current_file, relative_path)
    with open(config_path, "rb") as config_file:
        config = toml.load(config_file)
    if frozen:
        return make_immutable(config)
    else:
        return config
