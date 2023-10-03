import reflex as rx

from flexdown import types
from flexdown.blocks.block import Block


class CodeBlock(Block):
    """A block of code."""

    type = "code"
    starting_indicator = "```"
    ending_indicator = "```"
    include_indicators = True

    def render(self, env: types.Env, component_map: types.ComponentMap) -> rx.Component:
        return rx.markdown(self.get_content(env), component_map=component_map)
