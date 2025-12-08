"""
Database Connection (Shared across all backends)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.shared.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set False in production
    pool_pre_ping=True,
    pool_recycle=3600
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()