from pathlib import Path
import click


def get_plasnet_source_dir():
    return Path(__file__).parent


def get_libs_dir():
    return get_plasnet_source_dir() / "ext/libs"


class PathlibPath(click.Path):
    def convert(self, value, param, ctx):
        return Path(super().convert(value, param, ctx))


def distance_df_to_dict(df):
    df_as_dict = {}
    for _, row in df.iterrows():
        df_as_dict[(row["plasmid_1"], row["plasmid_2"])] = row["distance"]
        df_as_dict[(row["plasmid_2"], row["plasmid_1"])] = row["distance"]
    return df_as_dict