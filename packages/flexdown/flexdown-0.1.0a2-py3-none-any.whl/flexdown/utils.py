"""Utility functions for Flexdown."""

import glob
import re
from typing import Any

from flexdown import constants, errors, types


def get_flexdown_files(path: str) -> list[str]:
    """Recursively get the Flexdown files in a directory.

    Args:
        path: The path to the directory to search.

    Returns:
        The list of Flexdown files in the directory.
    """
    return glob.glob(f"{path}/**/*{constants.FLEXDOWN_EXTENSION}", recursive=True)


def evaluate_templates(line: str, env: types.Env):
    """Evaluate template expressions in a line of text.

    Args:
        line: The line of text to evaluate.
        env: The environment variables to use for evaluation.
    """
    # Regular expression for matching template placeholders (with escaping).
    template_regex = r"(?<!\\)(?<!\\\\){(?!\\)(.*?)(?<!\\)}"

    # Find all template placeholders in the line.
    matches = re.findall(template_regex, line)

    # Iterate over each template placeholder.
    for match in matches:
        try:
            # Evaluate the Python expression and replace the template placeholder
            eval_result = str(eval(match, env, env))
            line = line.replace("{" + match + "}", eval_result)
        except Exception as e:
            # If the evaluation fails, leave the template placeholder unchanged
            raise errors.TemplateEvaluationError(
                f"Failed to evaluate expression '{match}'"
            ) from e

    # Return the line with the template placeholders replaced.
    return line
