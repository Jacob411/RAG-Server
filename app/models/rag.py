from pydantic import BaseModel, Field
from typing import Dict, Any, List

class RagRequest(BaseModel):
    query: str = Field(..., description="Query to send to the RAG server")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "query": "What is machine learning?"
            }]
        }
    }

class RagResponse(BaseModel):
    results: List[Dict[str, Any]] = Field(..., description="Array of RAG results")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "results": [{
                    "content": "Machine learning is...",
                    "score": 0.95
                }]
            }]
        }
    }