"""Constants used in flexdown."""

# The extension for Flexdown files.
FLEXDOWN_EXTENSION = ".md"

# The Flexdown app directory.
FLEXDOWN_DIR = ".flexdown/flexd"
FLEXDOWN_FILE = f"{FLEXDOWN_DIR}/flexd/flexd.py"

# The default app template.
APP_TEMPLATE = """import flexdown
app = flexdown.app('{path}')
"""
