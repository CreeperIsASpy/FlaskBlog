from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, create_engine
from typing import Optional, List

engine: Optional[any] = None  # 共享的数据库引擎


def init_db_engine(uri: str):
    """
    根据配置创建数据库引擎，并赋值给全局的 engine 变量。
    这个函数只在 create_app 中被调用一次。
    """
    global engine

    # 2. 在这里可以添加更多 create_engine 的参数，比如连接池设置
    engine = create_engine(
        uri,
        echo=False,  # 建议在生产中设为 False，否则会输出 SQL 语句
    )


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
