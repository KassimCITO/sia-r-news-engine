from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from config import DB_URL
import logging

logger = logging.getLogger(__name__)

# Create engine
engine = create_engine(DB_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def init_db():
    """Initialize database tables.

    This function calls SQLAlchemy's create_all but traps common
    OperationalError cases (e.g., concurrent creation where a
    'table already exists' error can occur when multiple gunicorn
    workers attempt to create tables at the same time). The call
    is therefore resilient and idempotent.
    """
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError as oe:
        # SQLite may raise OperationalError if a table was created by
        # another process between the check and the create. Log and
        # continue so the application can proceed.
        logger.warning(f"OperationalError during init_db (ignored): {oe}")
    except Exception as e:
        # Re-raise unexpected exceptions
        logger.error(f"Unexpected error initializing DB: {e}")
        raise


def get_db_session():
    """Get a database session"""
    return SessionLocal()
