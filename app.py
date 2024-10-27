from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import requests
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename=f'logs/rag_api_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG API", description="API for managing RAG documents")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
BASE_URL = "http://localhost:7272"

class DocumentItem(BaseModel):
    id: str = Field(..., description="Document unique identifier")
    title: str = Field(..., description="Document title")
    user_id: str = Field(..., description="User identifier")
    type: str = Field(..., description="Document type (e.g., pdf, txt)")
    created_at: str = Field(..., description="Creation timestamp")

class DocumentsResponse(BaseModel):
    results: List[DocumentItem] = Field(..., description="Array of document items")


class DeleteResponse(BaseModel):
    success: bool
    message: str
    status_code: int

# Helper function for making HTTP requests
async def make_request(method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
    """
    Helper function to make HTTP requests to the RAG server
    """
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"Making {method} request to {url}")
    
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        try:
            return response.json()
        except:
            return response.text
    except Exception as e:
  
        logger.error(f"Request failed: {str(e)}")

        return {
            "success": False,
            "message": f"Request failed: {str(e)}",
            "status_code": 500
        }

@app.post("/documents/ingest")
async def ingest_files(file: UploadFile = File(...)):
    """
    Upload a file to the RAG server
    """
    logger.info(f"Uploading file: {file.filename}")
    
    try:
        files = {
            'files': (file.filename, await file.read(), file.content_type)
        }
        
        response = await make_request(
            "POST",
            "/v2/ingest_files",
            files=files
        )
        
        logger.info(f"File upload successful: {file.filename}")
        return response
        
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to upload file: {str(e)}",
            "status_code": 500
        }

@app.get("/documents", response_model=DocumentsResponse)
async def list_documents():
    """
    Get overview of all documents
    """
    logger.info("Fetching documents overview")
    
    try:
        response = await make_request("GET", "/v2/documents_overview")
        return response
        
    except Exception as e:
        logger.error(f"Failed to fetch documents: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to fetch documents: {str(e)}",
            "status_code": 500
        }

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
        
        # Try to get JSON response
        response = await make_request(
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
# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Check if the API is running and can connect to the RAG server
    """
    try:
        await make_request("GET", "/v2/documents_overview")
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
