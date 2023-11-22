"""This module provides utility functions."""

import logging
import tiktoken

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",
)

MODEL_TOKEN_LENGTH_MAPPING = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-1106": 16385,
    "gpt-4-1106-preview": 128000,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
}


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


class TokenCounter:
    """A class for counting tokens."""

    def __init__(self, model_name="gpt-3.5-turbo"):
        self.encoding = tiktoken.encoding_for_model(model_name)
        self.model_token_length = MODEL_TOKEN_LENGTH_MAPPING[model_name]

    def count_tokens(self, text):
        """Count the number of tokens in a text.

        Args:
            text (str): The text to count the tokens of.

        Returns:
            int: The number of tokens in the text.
        """
        token_count = len(self.encoding.encode(text))
        return token_count
