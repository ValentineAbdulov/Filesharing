from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    TEXT,
    CHAR,
    VARCHAR,
    INTEGER,
    REAL,
    Column,
    ForeignKey,
    Table,
    UniqueConstraint,
    BOOLEAN,

)
from sqlalchemy.dialects.postgresql import TIME
from sqlalchemy.sql import func
from datetime import datetime

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(VARCHAR(36), unique=True)
    password: Mapped[str] = mapped_column(TEXT)
    first_name: Mapped[str] = mapped_column(VARCHAR(36), nullable=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(36), nullable=True)

class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(VARCHAR(255), unique=False, nullable=False)
    expire_at: Mapped[datetime] = mapped_column(TIME, nullable=True)
    one_time: Mapped[bool] = mapped_column(BOOLEAN, nullable=False)
    link_code: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False)