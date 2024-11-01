from sqlalchemy import Column, String, DateTime
from datetime import datetime
from . import Base

class DocumentGroupItem(Base):
    __tablename__ = "document_group_items"
    
    group_id = Column(String, primary_key=True)
    document_id = Column(String, primary_key=True)
    added_at = Column(DateTime, default=datetime.utcnow)