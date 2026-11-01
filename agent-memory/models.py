from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserProfile(Base):

    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    mobile: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )