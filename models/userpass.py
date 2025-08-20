from pydantic import BaseModel, field_validator


class UserPassword(BaseModel):
    username: str
    password: str

    @field_validator("username")
    def validate_username(cls, v):
        if not 5 <= len(v) <= 40:
            raise ValueError("Username must be between 5 and 40 characters long.")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if not 8 <= len(v) < 80:
            raise ValueError("Password must be between 8 and 80 characters")
        return v
