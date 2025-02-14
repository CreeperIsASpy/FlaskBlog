from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str = Field(index=True)
    password_hash: str
    is_admin: bool = Field(default=False)

    posts: List["Post"] = Relationship(back_populates="author")
    comments: List["Comment"] = Relationship(back_populates="author")
    likes: List["Like"] = Relationship(back_populates="user")  # 用户点赞的博文

    # Flask-Login 所需的属性和方法
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str  # 原始 Markdown 内容
    html_content: str  # 解析后的 HTML 内容
    author_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    author: User = Relationship(back_populates="posts")
    comments: List["Comment"] = Relationship(back_populates="post")
    likes: List["Like"] = Relationship(back_populates="post")  # 博文的点赞


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str  # 原始 Markdown 内容
    html_content: str  # 解析后的 HTML 内容
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: int = Field(foreign_key="user.id")
    post_id: int = Field(foreign_key="post.id")

    author: User = Relationship(back_populates="comments")
    post: Post = Relationship(back_populates="comments")


class Like(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # 点赞用户
    post_id: int = Field(foreign_key="post.id")  # 被点赞的博文

    # 关系
    user: "User" = Relationship(back_populates="likes")
    post: "Post" = Relationship(back_populates="likes")
