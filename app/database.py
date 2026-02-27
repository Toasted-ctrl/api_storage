import os

from dotenv import load_dotenv

# func is function on the server side
# JSON data may be added by using dicts

from sqlalchemy import create_engine, Column, Integer, String, Boolean, JSON, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Loading all database requirements.
hostname = os.getenv("hostname")
database = os.getenv("database")
password = os.getenv("password")
username = os.getenv("user")
port = os.getenv("port")
db_type = os.getenv("db_type")
db_conn = os.getenv("db_connection")

database_url = f"{db_type}+{db_conn}://{username}:{password}@{hostname}:{port}/{database}"

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

    hashed_api_key = Column(String(150), primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)

class Users(base):
    __tablename__ = 'users'

    # Set unique=True to ensure email addresses can only be added once.
    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    is_admin = Column(Boolean, nullable=False)
    can_read = Column(Boolean, nullable=False)
    can_write = Column(Boolean, nullable=False)

class Ingest(base):
    __tablename__ = 'ingest'

    item_id = Column(Integer, primary_key=True)
    url_primary = Column(String(100), nullable=False)
    url_extension = Column(String(100), nullable=True)
    params = Column(JSON, nullable=True)
    status_code = Column(Integer, nullable=False)
    data = Column(JSON, nullable=False)

    # Will add datetime of when the entry was added on the server side.
    date_added = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)

#base.metadata.create_all(engine)