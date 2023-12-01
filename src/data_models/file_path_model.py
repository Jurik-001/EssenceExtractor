from pydantic import BaseModel, validator
import os


class FilePath(BaseModel):
    file_path: str

    @validator('file_path')
    def file_must_exist(cls, v):
        if not os.path.exists(v):
            raise ValueError(f'The file at {v} does not exist.')
        if not os.path.isfile(v):
            raise ValueError(f'The path {v} is not a file.')
        if not os.access(v, os.R_OK):
            raise ValueError(f'The file at {v} is not readable.')
        return v