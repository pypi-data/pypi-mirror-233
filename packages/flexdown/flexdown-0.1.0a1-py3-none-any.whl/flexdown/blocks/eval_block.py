import reflex as rx

from flexdown.blocks.block import Block


class EvalBlock(Block):
    """A block that evaluates a Reflex component to display."""

    type = "eval"
    starting_indicator = "```python eval"
    ending_indicator = "```"

    def render(self, env) -> rx.Component:
        return eval(self.get_content(env), env, env)
