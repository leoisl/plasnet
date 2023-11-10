from plasnet.utils import get_plasnet_source_dir


class Templates:
    @staticmethod
    def get_templates_dir():
        return get_plasnet_source_dir() / "ext/templates"

    @staticmethod
    def read_template(template_name):
        template_filepath = Templates.get_templates_dir() / (template_name + ".html")
        with open(template_filepath) as template_fh:
            template_src = template_fh.readlines()
        return list(map(lambda line: line.strip("\n"), template_src))
