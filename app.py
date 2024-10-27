from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

from r2r import R2RClient


# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request/response models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    context_id: Optional[str] = None

class DocumentUpload(BaseModel):
    content: str
    metadata: dict

# Initialize RAG client
rag_client = R2RClient("http://localhost:7272")

health_check = rag_client.health()
print(health_check)

# Chat endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        response = await rag_client.query(
            messages=request.messages,
            context_id=request.context_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Document upload endpoint
@app.post("/api/documents/upload")
async def upload_document(document: DocumentUpload):
    try:
        response = await rag_client.upload_document(
            content=document.content,
            metadata=document.metadata
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
