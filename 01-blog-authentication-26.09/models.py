from sqlalchemy.orm import relationship, Mapped, mapped_column
from werkzeug.security import generate_password_hash
from sqlalchemy import ForeignKey, Integer, String, Text
from flask_login import UserMixin
from extensions import db, login_manager


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column(ForeignKey("blog_posts_table.id"))
    parent_post: Mapped["BlogPost"] = relationship(back_populates="comments")
    text: Mapped[str] = mapped_column(Text)

    @classmethod
    def fetch_all(cls):
        return db.session.execute(db.select(cls)).scalars().all()


class BlogPost(db.Model):
    __tablename__ = "blog_posts_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="parent_post")
    title: Mapped[str] = mapped_column(String(250), unique=True)
    subtitle: Mapped[str] = mapped_column(String(250))
    date: Mapped[str] = mapped_column(String(250))
    body: Mapped[str] = mapped_column(Text)
    img_url: Mapped[str] = mapped_column(String(250))


class User(UserMixin, db.Model):
    __tablename__ = "users_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    posts: Mapped[list["BlogPost"]] = relationship(back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    email: Mapped[str] = mapped_column(String(250), unique=True)
    password: Mapped[str] = mapped_column(String(250))
    name: Mapped[str] = mapped_column(String(50))

    @classmethod
    def add_user_to_db(cls, email: str, password: str, name: str) -> None:
        new_user = User(email=email, password=generate_password_hash(password), name=name)  # type: ignore
        db.session.add(new_user)
        db.session.commit()

    @classmethod
    def fetch_from_database(cls, email: str) -> User:
        return db.session.execute(db.select(cls).where(cls.email == email)).scalar()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
