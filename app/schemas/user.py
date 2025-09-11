from pydantic import BaseModel, field_validator

from models import User


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


class UserDTO(BaseModel):
    id: int
    username: str
    avatar: str | None
    created_at: str

    @classmethod
    def from_db(self, user: User):
        if isinstance(user, User):
            return UserDTO(
                id=user.id,
                username=user.username,
                avatar=user.avatar,
                created_at=user.created_at.strftime("%d.%m.%Y %H:%M:%S"),
            )
        else:
            raise TypeError("User must be of type User")
