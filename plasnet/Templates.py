from plasnet.utils import get_plasnet_source_dir


class Templates:
    @staticmethod
    def get_templates_dir():
        return get_plasnet_source_dir() / "ext/templates"

    @staticmethod
    def read_template(template_filepath):
        with open(template_filepath) as template_fh:
            template_src = template_fh.readlines()
        return map(lambda line: line.strip("\n"), template_src)
