from os import path
import tomllib as toml


def load_relative(current_file, relative_path):
    script_path = path.abspath(current_file)
    script_dir = path.dirname(script_path)
    return path.join(script_dir, relative_path)


def load_config(current_file, relative_path):
    config_path = load_relative(current_file, relative_path)
    with open(config_path, "rb") as config_file:
        config = toml.load(config_file)
    return config
