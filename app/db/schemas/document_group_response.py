from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentGroupResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_by: str
    created_at: datetime
    document_ids: List[str]

    class Config:
        orm_mode = True