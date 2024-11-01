from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from . import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)  # matches R2R user ID
    email = Column(String, unique=True)
    subscription_tier = Column(String, default="free")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)