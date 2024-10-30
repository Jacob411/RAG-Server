from pydantic import BaseModel, Field
from typing import List

class DocumentItem(BaseModel):
    id: str = Field(..., description="Document unique identifier")
    title: str = Field(..., description="Document title")
    user_id: str = Field(..., description="User identifier")
    document_type: str = Field(..., description="Document type (e.g., pdf, txt)")
    created_at: str = Field(..., description="Creation timestamp")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": "doc123",
                "title": "Sample Document",
                "user_id": "user1",
                "document_type": "pdf",
                "created_at": "2024-03-21T10:00:00Z"
            }]
        }
    }

class DocumentsResponse(BaseModel):
    results: List[DocumentItem] = Field(..., description="Array of document items")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "results": [{
                    "id": "doc123",
                    "title": "Sample Document",
                    "user_id": "user1",
                    "document_type": "pdf",
                    "created_at": "2024-03-21T10:00:00Z"
                }]
            }]
        }
    }

class DeleteResponse(BaseModel):
    success: bool
    message: str
    status_code: int
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "success": True,
                "message": "Document deleted successfully",
                "status_code": 200
            }]
        }
    }