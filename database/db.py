from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base

DATABASE_URL = (
    "mssql+pyodbc://@localhost/FusionDB"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(
    DATABASE_URL,
    echo=True,
    fast_executemany=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()