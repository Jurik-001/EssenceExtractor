"""This module provides utility functions."""

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",
)


def save_to_md_file(content, file_path):
    """Save content to a markdown file.

    Args:
        content (str): The content to save.
        file_path (str): The path to the file to save to.

    Returns:
        str: The path to the saved file.
    """
    with open(file_path, "w") as f:
        f.write(content)
    logging.info(f"Blog post saved to: {file_path}")
    return file_path


def format_to_markdown(text):
    """Format text to markdown.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    lines = text.split("\\n")

    formatted_lines = []

    for line in lines:
        if line.startswith("#"):
            if formatted_lines:
                formatted_lines.append("")
        formatted_lines.append(line)

    formatted_text = "\n".join(formatted_lines)

    return formatted_text
