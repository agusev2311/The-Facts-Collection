from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database_connect import Base

class User(Base):
    __tablename__ = "users"

    uuid = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    telegram = Column(String)
    status = Column(String, default="OK")
    permission = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.now)

class Invite(Base):
    __tablename__ = "invites"

    uuid = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    telegram = Column(String, nullable=False)
    status = Column(String, default="not_used")
    created_at = Column(DateTime, default=datetime.now)
    used_at = Column(DateTime, default=datetime.now)