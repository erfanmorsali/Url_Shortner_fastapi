from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.session import Base

if TYPE_CHECKING:
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    urls = relationship("Url", back_populates="owner", cascade="all, delete")
    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)
    api_key = Column(String, unique=True, nullable=True)

