"""Constants used in flexdown."""

# The extension for Flexdown files.
FLEXDOWN_EXTENSION = ".md"

# The Flexdown app directory.
FLEXDOWN_DIR = ".flexdown/flexd"
FLEXDOWN_FILE = f"{FLEXDOWN_DIR}/flexd/flexd.py"
FLEXDOWN_MODULES_DIR = "modules"

# The default app template.
APP_TEMPLATE = """import flexdown
import reflex as rx
component_map = {{
    "a": lambda value, **props: rx.link(value, color="blue", **props),
}}
app = flexdown.app(
    '{path}',
    page_template=flexdown.templates.base_template,
    component_map=component_map
)
"""
