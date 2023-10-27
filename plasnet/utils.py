from pathlib import Path
import click


def get_plasnet_source_dir():
    return Path(__file__).parent


def get_libs_dir():
    return get_plasnet_source_dir() / "ext/libs"


class PathlibPath(click.Path):
    def convert(self, value, param, ctx):
        return Path(super().convert(value, param, ctx))
