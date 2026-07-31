from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True) # nullable for oauth users
    auth_provider = Column(String, default="local")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
