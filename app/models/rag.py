from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class RagRequest(BaseModel):
    query: str = Field(..., description="Query to send to the RAG server")
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "query": "What is machine learning?"
            }]
        }
    }

class ChatMessage(BaseModel):
    content: str
    refusal: Optional[Any] = None
    role: str
    audio: Optional[Any] = None
    function_call: Optional[Any] = None
    tool_calls: Optional[Any] = None

class ChatChoice(BaseModel):
    finish_reason: str
    index: int
    logprobs: Optional[Any]
    message: ChatMessage

class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    completion_tokens_details: Dict[str, Any]
    prompt_tokens_details: Dict[str, Any]

class ChatCompletion(BaseModel):
    id: str
    choices: List[ChatChoice]
    created: int
    model: str
    object: str
    service_tier: Optional[Any]
    system_fingerprint: str
    usage: Usage

class VectorSearchResult(BaseModel):
    extraction_id: str
    document_id: str
    user_id: str
    collection_ids: List[str]
    score: float
    text: str
    metadata: Dict[str, Any]

class SearchResults(BaseModel):
    vector_search_results: List[VectorSearchResult]
    kg_search_results: Optional[Any]

class RagResponseContent(BaseModel):
    completion: ChatCompletion
    search_results: SearchResults

class RagResponse(BaseModel):
    results: RagResponseContent

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "results": {
                    "completion": {
                        "id": "chatcmpl-123",
                        "choices": [{
                            "finish_reason": "stop",
                            "index": 0,
                            "message": {"content": "Response content..."}
                        }]
                    },
                    "search_results": {
                        "vector_search_results": [{
                            "text": "Relevant text...",
                            "score": 0.95
                        }]
                    }
                }
            }]
        }
    }