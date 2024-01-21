from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

user = 'postgres'
password = 'example'
host = 'localhost'
port = '5432'
database = 'mydb'
connection_str = f'postgresql://{user}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_str,
                       echo=True)

local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass