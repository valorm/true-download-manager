from celery import Celery
from datetime import timedelta
from typing import Optional, Dict, Any

from download_manager import DownloadManager
from media_extractor import MediaExtractor
from models.download import Download
from database import SessionLocal

# Initialize Celery app
app = Celery('true_download_manager')
app.config_from_object('celeryconfig')

# Initialize components
download_manager = DownloadManager()
media_extractor = MediaExtractor()

@app.task(bind=True, max_retries=3)
def process_download(self, download_id: int, url: str, options: Optional[Dict[Any, Any]] = None):
    """Process a download request asynchronously"""
    try:
        # Get database session
        db = SessionLocal()
        
        # Update download status to 'processing'
        download = db.query(Download).filter(Download.id == download_id).first()
        if not download:
            raise ValueError(f"Download with id {download_id} not found")
        
        download.status = 'processing'
        db.commit()
        
        # Start the download
        result = download_manager.start_download(url, options or {})
        
        # Update download with result
        download.status = 'completed'
        download.file_path = result.get('file_path')
        download.file_size = result.get('file_size')
        db.commit()
        
    except Exception as exc:
        # Update download status to 'failed'
        download.status = 'failed'
        download.error_message = str(exc)
        db.commit()
        
        # Retry the task
        raise self.retry(exc=exc, countdown=60)
    
    finally:
        db.close()

@app.task
def extract_media_info(download_id: int):
    """Extract media information from downloaded file"""
    try:
        db = SessionLocal()
        download = db.query(Download).filter(Download.id == download_id).first()
        
        if not download or not download.file_path:
            raise ValueError(f"Download {download_id} not found or has no file path")
        
        # Extract media information
        media_info = media_extractor.extract_info(download.file_path)
        
        # Update download with media information
        download.media_info = media_info
        db.commit()
        
    except Exception as e:
        # Log error but don't fail the task
        print(f"Error extracting media info for download {download_id}: {str(e)}")
    
    finally:
        db.close()

@app.task
def cleanup_old_downloads():
    """Periodic task to clean up old downloads"""
    try:
        db = SessionLocal()
        # Get old downloads (e.g., older than 30 days)
        old_downloads = db.query(Download).filter(
            Download.created_at < (datetime.utcnow() - timedelta(days=30))
        ).all()
        
        for download in old_downloads:
            # Delete file if it exists
            if download.file_path:
                try:
                    download_manager.delete_file(download.file_path)
                except Exception as e:
                    print(f"Error deleting file {download.file_path}: {str(e)}")
            
            # Delete download record
            db.delete(download)
        
        db.commit()
        
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")
    
    finally:
        db.close()

# Schedule periodic tasks
app.conf.beat_schedule = {
    'cleanup-old-downloads': {
        'task': 'celery_tasks.cleanup_old_downloads',
        'schedule': timedelta(days=1),  # Run daily
    },
}