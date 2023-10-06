from dataclasses import dataclass
from hashlib import md5
from pathlib import Path
from typing import List

from jinja2 import BaseLoader, Environment, Template, select_autoescape

from unireport.plugin import Plugin


@dataclass
class RenderContext:
    output: Path


class Unireport:
    def __init__(self, loader: BaseLoader | None = None):
        self.env = Environment(loader=loader, autoescape=select_autoescape())
        self.plugins: List[Plugin] = []
        self._current_ctx: RenderContext | None = None

    def get_context(self) -> RenderContext:
        return self._current_ctx

    def register(self, *args):
        for plugin in args:
            plugin: Plugin
            self.plugins.append(plugin)
            plugin.setup(self.get_context, self.env)

    def render_from_file(
        self,
        template_filename: str,
        data: {},
        output: Path = None,
    ):
        template = self.env.get_template(template_filename)
        return self._render(template, data, output)

    def render_from_string(
        self,
        template_string: str,
        data: {},
        output: Path = None,
    ):
        template = self.env.from_string(template_string)
        digest = md5(template_string.encode("utf-8")).hexdigest()
        template.name = f"template_{digest}"
        return self._render(template, data, output)

    def _render(self, template: Template, data: {}, output: Path | None):
        self._current_ctx = RenderContext(
            output=output,
        )
        try:
            result = template.render(data)
            if output:
                result_file = output / template.name
                with open(result_file, "w", encoding="utf8") as f:
                    f.write(result)

            return result
        finally:
            self._current_ctx = None
