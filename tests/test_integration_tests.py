from pathlib import Path
from unittest import TestCase

from click.testing import CliRunner

from plasnet.plasnet_main import cli


def check_if_files_are_equal(file_1: Path, file_2: Path, sort: bool = False) -> bool:
    with open(file_1) as fh1, open(file_2) as fh2:
        file1_contents = fh1.readlines()
        file2_contents = fh2.readlines()

        if sort:
            file1_contents.sort()
            file2_contents.sort()

        return file1_contents == file2_contents


class TestSplitCommand(TestCase):
    def test_split_command(self) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "split",
                "tests/data/plasmids.tsv",
                "tests/data/split_distances.tsv",
                "tests/data/out/split_out",
                "--distance-threshold",
                "0.6",
                "--bh-connectivity",
                "10",
                "--bh-neighbours-edge-density",
                "0.2",
                "--output-plasmid-graph",
            ],
        )
        self.assertEqual(result.exit_code, 0)


class TestTypeCommand(TestCase):
    def test_type_command(self) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "type",
                "tests/data/communities.pkl",
                "tests/data/type_distances.tsv",
                "tests/data/out/type_out",
                "--distance-threshold",
                "4",
                "--small-subcommunity-size-threshold",
                "4",
            ],
        )
        self.assertEqual(result.exit_code, 0)


class TestAddSampleHitsCommand(TestCase):
    def test_add_sample_hits_command(self) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "add-sample-hits",
                "tests/data/subcommunities.pkl",
                "tests/data/sample_hits.tsv",
                "tests/data/out/sample_hits_out",
            ],
        )
        self.assertEqual(result.exit_code, 0)


class TestRemoveHubPlasmidsIteratively(TestCase):
    def test_remove_hub_plasmids_iteratively(self) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "split",
                "tests/data/hub/plasmids.tsv",
                "tests/data/hub/all_pairs_jaccard_distance.tsv",
                "tests/data/hub/out/split_out",
                "--distance-threshold",
                "0.6",
                "--bh-connectivity",
                "10",
                "--bh-neighbours-edge-density",
                "0.2",
                "--output-plasmid-graph",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(
            cli,
            [
                "type",
                "tests/data/hub/out/split_out/objects/communities.pkl",
                "tests/data/hub/all_plasmids_distances.tsv",
                "tests/data/hub/out/type_out",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        self.assertTrue(
            check_if_files_are_equal(
                Path("tests/data/hub/out/type_out/objects/typing.tsv"),
                Path("tests/data/hub/truth_typing.tsv"),
                sort=True,
            )
        )
