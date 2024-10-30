from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

# Request Models
class VectorSearchSettings(BaseModel):
    use_vector_search: bool = Field(True, description="Whether to use vector search")
    use_hybrid_search: bool = Field(False, description="Whether to perform a hybrid search")
    search_filters: Optional[Dict[str, Any]] = Field(None, description="Filters to apply to the vector search")
    search_limit: int = Field(10, description="Maximum number of results to return")
    offset: int = Field(0, description="Offset to paginate search results")
    selected_collection_ids: Optional[List[str]] = Field(None, description="Collection IDs to search for")
    index_measure: Optional[str] = Field(None, description="The distance measure to use for indexing")
    include_values: bool = Field(True, description="Whether to include search score values")
    include_metadatas: bool = Field(True, description="Whether to include element metadata")
    probes: Optional[int] = Field(10, description="Number of ivfflat index lists to query")
    ef_search: Optional[int] = Field(40, description="Size of the dynamic candidate list for HNSW index search")
    hybrid_search_settings: Optional[Dict[str, Any]] = Field(None, description="Settings for hybrid search")
    search_strategy: str = Field("vanilla", description="Search strategy to use")

class KGSearchSettings(BaseModel):
    search_filters: Optional[Dict[str, Any]] = Field(None, description="Filters to apply to the search")
    selected_collection_ids: Optional[List[str]] = Field(None, description="Collection IDs to search for")
    graphrag_map_system_prompt: str = Field("graphrag_map_system_prompt", description="System prompt for graphrag map")
    graphrag_reduce_system_prompt: str = Field("graphrag_reduce_system_prompt", description="System prompt for graphrag reduce")
    use_kg_search: bool = Field(False, description="Whether to use KG search")
    kg_search_type: str = Field("local", description="KG search type")
    kg_search_level: Optional[str] = Field(None, description="KG search level")
    generation_config: Optional[Dict[str, Any]] = Field(None, description="Configuration for text generation")
    max_community_description_length: int = Field(65536, description="Max length for community descriptions")
    max_llm_queries_for_global_search: int = Field(250, description="Max LLM queries for global search")
    local_search_limits: Optional[Dict[str, Any]] = Field(None, description="Local search limits")

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    vector_search_settings: Optional[VectorSearchSettings] = Field(None, description="Vector search settings")
    kg_search_settings: Optional[KGSearchSettings] = Field(None, description="Knowledge graph search settings")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "query": "example search query",
                "vector_search_settings": {
                    "use_vector_search": True,
                    "search_limit": 10
                },
                "kg_search_settings": {
                    "use_kg_search": False
                }
            }]
        }
    }

# Response Models
class VectorSearchMetadata(BaseModel):
    version: str
    chunk_order: int
    document_type: str
    associated_query: str

class VectorSearchResult(BaseModel):
    extraction_id: str
    document_id: str
    user_id: str
    collection_ids: List[str]
    score: float
    text: str
    metadata: VectorSearchMetadata

class SearchResults(BaseModel):
    vector_search_results: List[VectorSearchResult]
    kg_search_results: Optional[Any] = None

class SearchResponse(BaseModel):
    results: SearchResults

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "results": {
                    "vector_search_results": [{
                        "extraction_id": "123",
                        "document_id": "456",
                        "user_id": "789",
                        "collection_ids": ["abc"],
                        "score": 0.95,
                        "text": "Sample content",
                        "metadata": {
                            "version": "v0",
                            "chunk_order": 0,
                            "document_type": "txt",
                            "associated_query": "query"
                        }
                    }],
                    "kg_search_results": None
                }
            }]
        }
    }