from pathlib import Path

import click
import pandas as pd


def get_plasnet_source_dir() -> Path:
    return Path(__file__).parent


def get_libs_dir() -> Path:
    return get_plasnet_source_dir() / "ext/libs"


class PathlibPath(click.Path):
    def convert(self, value: str, param, ctx) -> Path:
        return Path(super().convert(value, param, ctx))


DistanceDict = dict[tuple[str, str], float]


def distance_df_to_dict(df: pd.DataFrame) -> DistanceDict:
    df_as_dict = {}
    for _, row in df.iterrows():
        df_as_dict[(row["plasmid_1"], row["plasmid_2"])] = row["distance"]
        df_as_dict[(row["plasmid_2"], row["plasmid_1"])] = row["distance"]
    return df_as_dict
