import uuid

from sqlalchemy import TIMESTAMP, Column, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy.schema import ForeignKey


@as_declarative()
class Base:
    """Base model."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False, onupdate=func.current_timestamp()
    )
    __name__: str


class User(Base):
    """User DB model."""

    username = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100))
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(70), nullable=False)
    posts = relationship("Post", back_populates="author")
    likes = relationship("Like", back_populates="user")

    def __repr__(self):
        return f"User (username: {self.username}, email: {self.email})"


class Post(Base):
    """Post DB model."""

    title = Column(String(500), nullable=False)
    text = Column(String, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    author = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")

    def __repr__(self):
        return self.title


class Like(Base):
    """Model for posts likes storage."""

    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="likes")
    post_id = Column(UUID(as_uuid=True), ForeignKey(Post.id, ondelete="CASCADE"), nullable=False)
    post = relationship("Post", back_populates="likes")

    def __repr__(self):
        return self.title
