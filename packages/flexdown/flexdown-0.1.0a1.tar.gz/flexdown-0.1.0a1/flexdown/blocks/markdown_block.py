from typing import Any, Callable

import reflex as rx

from flexdown.blocks.block import Block


class MarkdownBlock(Block):
    """A block of Markdown."""

    type = "markdown"

    # The function to use to render the Markdown.
    markdown_fn: Callable[[str], rx.Component] = rx.markdown

    def render(self, env: dict[str, Any]) -> rx.Component:
        return self.markdown_fn(self.get_content(env))
