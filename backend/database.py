from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# You should replace this with your actual database URL in production
DATABASE_URL = "sqlite:///./true_download_manager.db"

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    max_overflow=10,
    pool_size=5,
    pool_timeout=30,
    pool_recycle=1800,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for SQLAlchemy models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database tables
def init_db():
    Base.metadata.create_all(bind=engine)