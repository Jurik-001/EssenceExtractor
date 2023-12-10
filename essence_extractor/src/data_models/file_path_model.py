"""Data model for a file path."""

import os

from pydantic import BaseModel, validator


class FilePath(BaseModel):
    """Data model for a file path."""
    file_path: str

    @validator('file_path')
    def file_must_exist(cls, v):
        """Validate that the file exists and is readable."""
        if not os.path.exists(v):
            raise ValueError(f'The file at {v} does not exist.')
        if not os.path.isfile(v):
            raise ValueError(f'The path {v} is not a file.')
        if not os.access(v, os.R_OK):
            raise ValueError(f'The file at {v} is not readable.')
        return v