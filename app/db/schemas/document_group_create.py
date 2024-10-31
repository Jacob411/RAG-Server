from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentGroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
    document_ids: List[str]