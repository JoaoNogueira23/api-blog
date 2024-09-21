from sqlalchemy import String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from datetime import datetime, date

Base = declarative_base()


class Post(Base):
    __tablename__ = 'tb_posts'
    postId: Mapped[str] = mapped_column(String(255), primary_key=True)
    rawText: Mapped[str] = mapped_column(String(255)) 
    publishedDate: Mapped[datetime] = mapped_column(DateTime(timezone=True))  # Inclui fuso horário
    ingestionDate: Mapped[datetime] = mapped_column(DateTime(timezone=True))  # Inclui fuso horário
    author: Mapped[str] = mapped_column(String(100))
    userId: Mapped[str] = mapped_column(ForeignKey('tb_users.userId'))  # Chave estrangeira para `tb_users`
    title: Mapped[str] = mapped_column(String(64))
    subTitle: Mapped[str] = mapped_column(String(64), nullable=True)
    imgUrlPost: Mapped[str] = mapped_column(String())
    user: Mapped["User"] = relationship("User", back_populates="post")  # Removido `delete-orphan`

    class Config:
        from_attributes = True


class User(Base):
    __tablename__ = 'tb_users'
    userId: Mapped[str] = mapped_column(String(100), primary_key=True)
    username: Mapped[str] = mapped_column(String(160), nullable=False)
    birthdayDate: Mapped[date] = mapped_column(Date)
    usermail: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(255))
    userType: Mapped[str] = mapped_column(String(20))
    post: Mapped[List["Post"]] = relationship("Post", back_populates="user", 
                                              cascade="all, delete-orphan")  # `delete-orphan` aplicado aqui
    class Config:
        from_attributes = True