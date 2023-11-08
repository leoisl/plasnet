from plasnet.blackhole_graph import BlackholeGraph


class SubcommunityGraph(BlackholeGraph):
    def _get_libs_relative_path(self) -> str:
        return ".."

    def _get_samples_selectors_HTML(self) -> str:
        return ""

