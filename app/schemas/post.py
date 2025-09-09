from pydantic import BaseModel, field_validator


class PostData(BaseModel):
    author_id: int
    text: str

    @field_validator("author_id")
    def validate_id(cls, v):
        if v < 0:
            raise ValueError("Id must be a positive number.")
        return v

    @field_validator("text")
    def validate_text(cls, v):
        if not 0 < len(v) <= 1000:
            raise ValueError("Text must be between 1 and 1000 characters long.")
        return v
