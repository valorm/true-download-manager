from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Download(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    url = Column(String)
    file_name = Column(String)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String, nullable=True)
    status = Column(String)  # pending, downloading, completed, failed, paused
    progress = Column(Float, default=0.0)
    download_path = Column(String)
    checksum = Column(String, nullable=True)
    download_speed = Column(Float, nullable=True)  # bytes per second
    threads = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Metadata for media extraction
    media_info = Column(String, nullable=True)  # JSON string for media metadata
    
    # Relationship with User
    user = relationship("User", back_populates="downloads")