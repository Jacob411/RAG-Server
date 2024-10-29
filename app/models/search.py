from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

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
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "use_vector_search": True,
                "search_limit": 10,
                "search_strategy": "vanilla"
            }]
        }
    }

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
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "use_kg_search": False,
                "kg_search_type": "local"
            }]
        }
    }

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

class SearchResult(BaseModel):
    id: str = Field(..., description="Result identifier")
    score: float = Field(..., description="Search result score")
    content: str = Field(..., description="Result content")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Result metadata")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": "doc123",
                "score": 0.95,
                "content": "Sample content",
                "metadata": {"source": "document1.pdf"}
            }]
        }
    }

class SearchResponse(BaseModel):
    vector_search_results: List[SearchResult] = Field(..., description="List of vector search results")
    kg_search_results: Optional[List[SearchResult]] = Field(None, description="Knowledge graph search results, if applicable")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "vector_search_results": [{
                    "id": "doc123",
                    "score": 0.95,
                    "content": "Sample content",
                    "metadata": {"source": "document1.pdf"}
                }],
                "kg_search_results": None
            }]
        }
    }