"""Define shared functionality for the routers."""
from pydantic import BaseModel, ConfigDict


def to_camel_case(text: str) -> str:
    words = text.replace('-', ' ').replace('_', ' ').split()
    camel_cased_words = [words[0].lower()] + [word.capitalize() for word in words[1:]]
    return ''.join(camel_cased_words)



class BaseAPIModel(BaseModel):
    """Define the base model for all API models."""

    model_config = ConfigDict(
        alias_generator=to_camel_case,
        populate_by_name=True,
    )
