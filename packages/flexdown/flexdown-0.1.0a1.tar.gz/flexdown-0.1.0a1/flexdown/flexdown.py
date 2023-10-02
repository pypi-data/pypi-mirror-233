from typing import Callable

import reflex as rx

from flexdown import utils
from flexdown.blocks import Block, MarkdownBlock, CodeBlock, ExecBlock, EvalBlock


class Flexdown(rx.Base):
    """Class to parse and render flexdown files."""

    # The list of accepted block types to parse.
    blocks: list[type[Block]] = [
        ExecBlock,
        EvalBlock,
        CodeBlock,
        MarkdownBlock,
    ]

    # The default block type.
    default_block_type: type[Block] = MarkdownBlock

    # The template to use when rendering pages.
    page_template: Callable[[rx.Component], rx.Component] = lambda page: rx.container(
        page, margin_y="5em"
    )

    def _get_block(self, line: str) -> Block:
        """Get the block type for a line of text.

        Args:
            line: The line of text to check.

        Returns:
            The block type for the line of text.
        """
        # Search for a block type that can parse the line.
        for block_type in self.blocks:

            # Try to create a block from the line.
            block = block_type.from_line(line)

            # If a block was created, then return it.
            if block is not None:
                return block

        # If no block was created, then return the default block type.
        return self.default_block_type().append(line)

    def get_blocks(self, source: str) -> list[Block]:
        """Parse a Flexdown file into blocks.

        Args:
            source: The source code of the Flexdown file.

        Returns:
            The list of blocks in the Flexdown file.
        """
        # The list of parsed blocks.
        blocks: list[Block] = []
        current_block = None

        # Iterate over each line in the source code.
        for line in source.splitlines():

            # If there is no current block, then create a new block.
            if current_block is None:
                # If the line is empty, then skip it.
                if line == "":
                    continue

                # Otherwise, create a new block.
                current_block = self._get_block(line)

            # Add the line to the current block.
            current_block.append(line)

            # Check if the current block is finished.
            if current_block.is_finished():
                blocks.append(current_block)
                current_block = None

        # Add the final block if it exists.
        if current_block is not None:
            blocks.append(current_block)

        # Return the list of blocks.
        return blocks

    def render(self, source: str) -> rx.Component:
        """Render a Flexdown file into a Reflex component.

        Args:
            source: The source code of the Flexdown file.

        Returns:
            The Reflex component representing the Flexdown file.
        """
        # The environment used for execing and evaling code.
        env = {}

        # Render each block.
        return self.page_template(
            rx.fragment(*[block.render(env) for block in self.get_blocks(source)])
        )

    def render_file(self, path: str) -> rx.Component:
        """Render a Flexdown file into a Reflex component.

        Args:
            path: The path to the Flexdown file.

        Returns:
            The Reflex component representing the Flexdown file.
        """
        # Render the source code.
        return self.render(open(path, "r").read())

    def create_app(self, path: str) -> rx.App:
        """Create a Reflex app from a directory of Flexdown files.

        Args:
            path: The path to the directory of Flexdown files.

        Returns:
            The Reflex app representing the directory of Flexdown files.
        """
        # Get all the flexdown files in the directory.
        files = utils.get_flexdown_files(path)

        # Create the Reflex app.
        app = rx.App()

        # Create a base state.
        class State(rx.State):
            pass

        # Add each page to the app.
        for file in files:
            route = file.replace(path, "").replace(".md", "")
            app.add_page(self.render_file(file), route=route)

        # Compile the app.
        app.compile()

        # Return the app.
        return app
