from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Optional fields for user profile
    full_name = Column(String, nullable=True)
    preferences = Column(String, nullable=True)  # JSON string for user preferences
    last_login = Column(DateTime, nullable=True)

    downloads = relationship("Download", back_populates="user", cascade="all, delete-orphan")
