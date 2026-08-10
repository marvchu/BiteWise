from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    website_url: Mapped[Optional[str]] = mapped_column(String(2048))
    source_url: Mapped[Optional[str]] = mapped_column(String(2048))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    locations: Mapped[list["Location"]] = relationship(
        back_populates="restaurant",
        cascade="all, delete-orphan",
    )
    menu_items: Mapped[list["MenuItem"]] = relationship(
        back_populates="restaurant",
        cascade="all, delete-orphan",
    )
