"""This module provides utility functions."""

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",
)


def save_to_md_file(content, file_path):
    with open(file_path, "w") as f:
        f.write(content)
    logging.info(f"Blog post saved to: {file_path}")
    return file_path
