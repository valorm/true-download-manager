import asyncio
import aiohttp
import os
from typing import Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DownloadProgress:
    filename: str
    total_size: int
    downloaded: int
    speed: float
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None

class DownloadManager:
    def __init__(self, max_concurrent_downloads: int = 3, chunk_size: int = 1024 * 1024):
        self.max_concurrent_downloads = max_concurrent_downloads
        self.chunk_size = chunk_size
        self.active_downloads: Dict[str, DownloadProgress] = {}
        self.semaphore = asyncio.Semaphore(max_concurrent_downloads)

    async def download_file(self, url: str, destination: str, headers: Optional[Dict] = None) -> DownloadProgress:
        async with self.semaphore:
            try:
                async with aiohttp.ClientSession(headers=headers) as session:
                    async with session.get(url) as response:
                        if response.status != 200:
                            raise Exception(f"Failed to download file: {response.status}")

                        total_size = int(response.headers.get('content-length', 0))
                        filename = os.path.basename(destination)
                        progress = DownloadProgress(
                            filename=filename,
                            total_size=total_size,
                            downloaded=0,
                            speed=0.0,
                            status='downloading',
                            started_at=datetime.now()
                        )
                        self.active_downloads[url] = progress

                        os.makedirs(os.path.dirname(destination), exist_ok=True)
                        start_time = asyncio.get_event_loop().time()

                        with open(destination, 'wb') as f:
                            async for chunk in response.content.iter_chunked(self.chunk_size):
                                if chunk:
                                    f.write(chunk)
                                    progress.downloaded += len(chunk)
                                    elapsed = asyncio.get_event_loop().time() - start_time
                                    if elapsed > 0:
                                        progress.speed = progress.downloaded / elapsed

                        progress.status = 'completed'
                        progress.completed_at = datetime.now()
                        return progress

            except Exception as e:
                if url in self.active_downloads:
                    self.active_downloads[url].status = 'failed'
                raise e

    def get_download_progress(self, url: str) -> Optional[DownloadProgress]:
        return self.active_downloads.get(url)

    def get_all_downloads(self) -> List[DownloadProgress]:
        return list(self.active_downloads.values())

    async def cancel_download(self, url: str) -> bool:
        if url in self.active_downloads:
            self.active_downloads[url].status = 'cancelled'
            return True
        return False

# Create a global instance of the download manager
download_manager = DownloadManager()