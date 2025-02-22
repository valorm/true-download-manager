# Celery Configuration

# Broker settings
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

# Task settings
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'

# Task routes
task_routes = {
    'celery_tasks.process_download': {'queue': 'downloads'},
    'celery_tasks.extract_media_info': {'queue': 'media'},
    'celery_tasks.cleanup_old_downloads': {'queue': 'maintenance'}
}

# Configure Celery Beat schedule
from datetime import timedelta

beat_schedule = {
    'cleanup-old-downloads': {
        'task': 'celery_tasks.cleanup_old_downloads',
        'schedule': timedelta(days=1),  # Run once per day
        'options': {'queue': 'maintenance'}
    }
}

# Worker settings
worker_prefetch_multiplier = 1  # Disable prefetching for better task distribution
worker_max_tasks_per_child = 1000  # Restart worker after 1000 tasks
worker_send_task_events = True  # Required for task monitoring

# Security settings
security_key = 'your-secret-key'  # Change this in production

# Task execution settings
task_acks_late = True  # Tasks are acknowledged after execution
task_reject_on_worker_lost = True  # Reject tasks if worker connection is lost
task_track_started = True  # Track when tasks are started by a worker