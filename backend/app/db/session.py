from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# 1. Create the SQLAlchemy Database Engine
# connect_args={"check_same_thread": False} is ONLY needed for SQLite
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# 2. creates a SessionLocal class. Each instance will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 3. creates a Base class for our models to inherit from
class Base(DeclarativeBase):
    pass


# 4. dependency function to get a Database Session for each HTTP request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Always close the connection when the request finishes!