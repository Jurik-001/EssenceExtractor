from pydantic import BaseModel, validator
from src.utils import MODEL_TOKEN_LENGTH_MAPPING
from typing import List


class LlmModelName(BaseModel):
    llm_name: str

    valid_model_names: List[str] = list(MODEL_TOKEN_LENGTH_MAPPING.keys())

    @validator('llm_name')
    def validate_model_name(cls, v):
        print("Att test LOL")
        if v not in cls.valid_model_names:
            raise ValueError(f"Invalid model name: {v}. Must be one of {cls.valid_model_names}")
        return v
