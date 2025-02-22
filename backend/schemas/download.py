from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DownloadBase(BaseModel):
    url: str
    file_name: str
    download_path: str
    threads: Optional[int] = 1

class DownloadCreate(DownloadBase):
    user_id: int

class DownloadUpdate(BaseModel):
    status: Optional[str] = None
    progress: Optional[float] = None
    download_speed: Optional[float] = None
    threads: Optional[int] = None

class DownloadInDB(DownloadBase):
    id: int
    user_id: int
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    status: str
    progress: float
    checksum: Optional[str] = None
    download_speed: Optional[float] = None
    media_info: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class DownloadOut(DownloadInDB):
    pass