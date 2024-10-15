from sqlalchemy import String, DateTime, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date

Base = declarative_base()


class User(Base):
    __tablename__ = 'tb_users'
    userId: Mapped[str] = mapped_column(String(100), primary_key=True)
    username: Mapped[str] = mapped_column(String(160), nullable=False)
    birthdayDate: Mapped[date] = mapped_column(Date)
    usermail: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(255))
    userType: Mapped[str] = mapped_column(String(20))
    class Config:
        from_attributes = True

class Post(Base):
    __tablename__ = 'tb_posts'
    postId: Mapped[str] = mapped_column(String(255), primary_key=True)
    rawText: Mapped[str] = mapped_column(Text) 
    publishedDate: Mapped[datetime] = mapped_column(DateTime(timezone=True))  # Inclui fuso horário
    acthor: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(255))
    resume: Mapped[str] = mapped_column(String(255), nullable=True)
    urlImage: Mapped[str] = mapped_column(String(255))

    class Config:
        from_attributes = True
    