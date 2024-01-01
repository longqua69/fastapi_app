from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine("sqlite+pysqlite:///:memory:",
                       echo=True,
                       connect_args={"check_same_thread": False})

local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass