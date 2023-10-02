from typing import Any

import reflex as rx

from flexdown.blocks.block import Block


class ExecBlock(Block):
    """A block of executable Python code."""

    type = "exec"
    starting_indicator = "```python exec"
    ending_indicator = "```"

    def render(self, env: dict[str, Any]) -> rx.Component:
        # Execute the code.
        exec(self.get_content(env), env, env)

        # Return an empty component.
        return rx.fragment()
