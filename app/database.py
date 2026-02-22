import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

hostname = os.getenv("hostname")
database = os.getenv("database")
password = os.getenv("password")
username = os.getenv("user")
port = os.getenv("port")

database_url = f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}"

engine = create_engine(url=database_url)
db_session = sessionmaker(autocommit = False, autoflush = False, bind = engine)
base = declarative_base()

def get_database():
    database = db_session()
    try:
        yield database
    finally:
        database.close()

class ApiKeys(base):
    __tablename__ = 'api_keys'

    api_key = Column(String(150), primary_key=True, nullable=False)
    id = Column(Integer, nullable=False)

class Users(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    is_admin = Column(Boolean, nullable=False)
    can_read = Column(Boolean, nullable=False)
    can_write = Column(Boolean, nullable=False)

#base.metadata.create_all(engine)