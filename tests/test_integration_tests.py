from unittest import TestCase

from click.testing import CliRunner

from plasnet.plasnet_main import cli


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
