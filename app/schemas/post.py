from pydantic import BaseModel, field_validator
import markdown2

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
    author_id: int
    author_username: str
    author_avatar: str | None
    created_at: str

    @classmethod
    def from_db(self, post: Post, formatted: bool = True):
        if isinstance(post, Post):
            if formatted:
                text = markdown2.markdown(post.text, extras=["breaks"])
            else:
                text = post.text
            return PostDTO(
                id=post.id,
                text=text,
                author_id=post.author_obj.id,
                author_username=post.author_obj.username,
                author_avatar=post.author_obj.avatar or None,
                created_at=post.created_at.strftime("%d.%m.%Y %H:%M:%S"),
            )
        else:
            raise TypeError("Post must be of type Post")
