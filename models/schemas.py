from sqlalchemy import Column, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date
from typing import List
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()


class PostSchemaOut(BaseModel):
    postId: str
    rawText: str
    publishedDate: datetime
    ingestionDate: datetime
    author: str
    userId: str
    title: str
    subTitle: str
    imgUrlPost: str

    class Config:
        orm_mode = True

class Post(Base):
    __tablename__ = 'tb_posts'
    postId: Mapped[str] = mapped_column(String(255), primary_key=True)
    rawText: Mapped[str] = mapped_column(String(255)) 
    publishedDate: Mapped[datetime] = mapped_column(DateTime(timezone=True))  # Inclui fuso horário
    ingestionDate: Mapped[datetime] = mapped_column(DateTime(timezone=True))  # Inclui fuso horário
    author: Mapped[str] = mapped_column(String(255))
    userId: Mapped[str] = mapped_column(ForeignKey('tb_users.userId'))  # Chave estrangeira para `tb_users`
    title: Mapped[str] = mapped_column(String(255))
    subTitle: Mapped[str] = mapped_column(String(255))
    imgUrlPost: Mapped[str] = mapped_column(String(255))
    user: Mapped["User"] = relationship("User", back_populates="post")  # Removido `delete-orphan`

    class Config:
        orm_mode = True


class User(Base):
    __tablename__ = 'tb_users'
    userId: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    birthdayDate: Mapped[date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    userType: Mapped[str] = mapped_column(String(255))
    post: Mapped[List["Post"]] = relationship("Post", back_populates="user", 
                                              cascade="all, delete-orphan")  # `delete-orphan` aplicado aqui
    class Config:
        orm_mode = True