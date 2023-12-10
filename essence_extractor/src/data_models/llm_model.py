"""Data model for LLM model name."""

from typing import ClassVar, List

from pydantic import BaseModel, validator

from essence_extractor.src.utils import MODEL_TOKEN_LENGTH_MAPPING


class LlmModelName(BaseModel):
    """Data model for model name."""
    llm_name: str

    valid_model_names: ClassVar[List[str]] = list(MODEL_TOKEN_LENGTH_MAPPING.keys())

    @validator('llm_name')
    def validate_model_name(cls, v):
        """Validate that the model name is valid."""
        if v not in cls.valid_model_names:
            raise ValueError(f"Invalid model name: {v}. "
                             f"Must be one of {cls.valid_model_names}")
        return v
