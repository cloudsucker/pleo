from pydantic import BaseModel, field_validator

from models import Post


class PostContent(BaseModel):
    text: str

    @field_validator("text")
    def validate_text(cls, v):
        if not 0 < len(v) <= 1000:
            raise ValueError("Text must be between 1 and 1000 characters long.")
        return v


class PostDTO(BaseModel):
    id: int
    text: str
    author_username: str
    created_at: str

    @classmethod
    def from_db(self, post: Post):
        if isinstance(post, Post):
            return PostDTO(
                id=post.id,
                text=post.text,
                author_username=post.author_obj.username,
                created_at=post.created_at.strftime("%d.%m.%Y %H:%M:%S"),
            )
        else:
            raise TypeError("Post must be of type Post")
