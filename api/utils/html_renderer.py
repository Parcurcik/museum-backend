from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader


class HTMLRenderer:
    def __init__(self, template_folder: str = "api/templates") -> None:
        self.env = Environment(loader=FileSystemLoader(template_folder))

    def render_template(
        self, context: Dict[str, Any], template_name: str = "email.html"
    ) -> str:
        template = self.env.get_template(template_name)
        return template.render(context)


html_renderer = HTMLRenderer()


def generate_mailing(mailing_dict: Dict[str, Any]) -> str:
    return html_renderer.render_template(mailing_dict)
