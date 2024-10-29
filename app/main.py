from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import requests
import json
import logging
from datetime import datetime

from app.models.document import DocumentItem, DocumentsResponse, DeleteResponse
from app.models.rag import RagRequest, RagResponse
from app.models.search import SearchRequest, SearchResponse
from app.utils.http import make_request
from app.config import get_settings

# Setup logging
logging.basicConfig(
    filename=f'logs/rag_api_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(title="RAG API", description="API for managing RAG documents")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints
@app.post("/rag", response_model=RagResponse)
async def rag(request: RagRequest):
    """
    Send a query to the RAG server
    """
    logger.info(f"Sending query to RAG: {request}")
    
    try:
        response = await make_request(
            settings.base_url,
            "POST",
            "/v2/rag",
            data=json.dumps({"query": request.query}),
            headers={"Content-Type": "application/json"}
        )
        
        if isinstance(response, dict) and not response.get("success", True):
            raise HTTPException(
                status_code=response.get("status_code", 500),
                detail=response.get("message", "RAG query failed")
            )
        
        return response
        
    except Exception as e:
        logger.error(f"RAG query failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"RAG query failed: {str(e)}"
        )

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Execute a search query against the RAG server with support for vector and knowledge graph search
    """
    logger.info(f"Processing search request: {request.query}")
    
    try:
        payload = request.model_dump(exclude_none=True, exclude_unset=True)

        response = await make_request(
            settings.base_url,
            method="POST",
            endpoint="/v2/search",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )

        if isinstance(response, dict) and not response.get("success", True):
            logger.error(f"Search request failed: {response.get('message')}")
            raise HTTPException(
                status_code=response.get("status_code", 500),
                detail=response.get("message", "Search request failed")
            )

        logger.info("Search request completed successfully")
        return SearchResponse(**response)

    except Exception as e:
        logger.error(f"Search operation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Search operation failed: {str(e)}"
        )

@app.post("/documents/ingest")
async def ingest_files(files: List[UploadFile] = File(...)):
    """
    Upload multiple files to the RAG server
    """
    try:
        results = []
        for file in files:
            logger.info(f"Uploading file: {file.filename}")
            files_dict = {
                'files': (file.filename, await file.read(), file.content_type)
            }
            
            response = await make_request(
                settings.base_url,
                "POST",
                "/v2/ingest_files",
                files=files_dict
            )
            results.append(response)
        
        logger.info("All files uploaded successfully")
        return results
        
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload files: {str(e)}"
        )

@app.get("/documents", response_model=DocumentsResponse)
async def list_documents():
    """
    Get overview of all documents
    """
    logger.info("Fetching documents overview")
    try:
        response = await make_request(
            settings.base_url,
            "GET",
            "/v2/documents_overview"
        )
        return response
    except Exception as e:
        logger.error(f"Failed to fetch documents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch documents: {str(e)}"
        )

@app.delete("/documents/{document_id}", response_model=DeleteResponse)
async def delete_document(document_id: str):
    """
    Delete a document by ID
    """
    logger.info(f"Deleting document: {document_id}")
    
    try:
        filters = {
            "document_id": {
                "$eq": document_id
            }
        }
        
        params = {
            "filters": json.dumps(filters)
        }
        
        response = await make_request(
            settings.base_url,
            "DELETE",
            "/v2/delete",
            params=params
        )
            
        logger.info(f"Document deleted successfully: {document_id}")
        return DeleteResponse(
            success=True,
            message=f"{document_id} deleted",
            status_code=200
        )
        
    except Exception as e:
        logger.error(f"Unexpected error during file delete: {str(e)}")
        return DeleteResponse(
            success=False,
            message=f"Failed to delete document: {str(e)}",
            status_code=500
        )

@app.get("/health")
async def health_check():
    """
    Check if the API is running and can connect to the RAG server
    """
    try:
        await make_request(
            settings.base_url,
            "GET", 
            "/v2/documents_overview"
        )
        return {"status": "healthy", "rag_server": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "rag_server": "disconnected",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)