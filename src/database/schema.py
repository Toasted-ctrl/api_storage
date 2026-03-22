from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, func
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class ApiKeys(Base):
    __tablename__ = 'api_keys'

    hashed_api_key = Column(String(150), primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    is_valid = Column(Boolean, nullable=False)
    inserted = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)

class Users(Base):
    __tablename__ = 'users'

    # Set unique=True to ensure email addresses can only be added once.
    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    is_admin = Column(Boolean, nullable=False)
    can_read = Column(Boolean, nullable=False)
    can_write = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)

class Ingest(Base):
    __tablename__ = 'ingest'

    item_id = Column(Integer, primary_key=True)
    base_url = Column(String(100), nullable=False)
    url_ext = Column(String(100), nullable=True)
    params = Column(JSON, nullable=True)
    status_code = Column(Integer, nullable=True)
    type = Column(String(10), nullable=True)
    data = Column(JSON, nullable=True)
    inserted = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)