from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database connection URL
# Format: dialect+driver://username:password@host:port/database_name
from app.core.config import DATABASE_URL
# The engine manages the actual connection pool to the database
engine = create_engine(DATABASE_URL, echo=False)  # Set echo=True for SQL query logging

# SessionLocal is a factory that creates new database sessions on demand
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is what all our model classes (Employee, User, etc.) will inherit from
Base = declarative_base()


def get_db():
    """
    Dependency function used by FastAPI routes.
    Opens a new DB session per request, and closes it afterward.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()