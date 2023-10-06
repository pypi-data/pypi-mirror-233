from jinja2 import Environment


class Plugin:
    def __init__(self):
        self._ctx_getter = None

    def setup(self, context_getter, _: Environment):
        self._ctx_getter = context_getter

    def get_context(self):
        return self._ctx_getter()
