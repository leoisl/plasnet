from pathlib import Path


def get_plasnet_source_dir():
    return Path(__file__).parent


def get_libs_dir():
    return get_plasnet_source_dir() / "ext/libs"
