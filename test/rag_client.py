from typing import Any, Dict
import requests
import os


class RAGClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the RAG client with a base URL"""
        self.base_url = base_url.rstrip('/')

    def ingest_file(self, file_path: str) -> Dict[str, Any]:
        """
        Ingest a file to the RAG server
        
        Args:
            file_path: Path to the file to be ingested
            
        Returns:
            Dict containing the response from the server
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(file_path, 'rb') as f:
            files = {'files': ('filename', f, 'application/octet-stream')}
            response = requests.post(f"{self.base_url}/documents/ingest", files=files)
            response.raise_for_status()
            return response.json()

    def list_documents(self) -> Dict[str, Any]:
        """
        Get list of all documents
        
        Returns:
            Dict containing the list of documents
        """
        response = requests.get(f"{self.base_url}/documents")
        response.raise_for_status()
        return response.json()

    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """
        Delete a document by ID
        
        Args:
            document_id: ID of the document to delete
            
        Returns:
            Dict containing the deletion response
        """
        response = requests.delete(f"{self.base_url}/documents/{document_id}")
        return response.json()

    def check_health(self) -> Dict[str, Any]:
        """
        Check API health
        
        Returns:
            Dict containing health status information
        """
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

    def search(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a search query
        
        Args:
            query: Search query string
            **kwargs: Additional search parameters
            
        Returns:
            Dict containing search results
        """
        payload = {"query": query, **kwargs}
        response = requests.post(f"{self.base_url}/search", json=payload)
        response.raise_for_status()
        return response.json()

    def rag_query(self, query: str) -> Dict[str, Any]:
        """
        Execute a RAG query
        
        Args:
            query: RAG query string
            
        Returns:
            Dict containing RAG response
        """
        payload = {"query": query}
        response = requests.post(f"{self.base_url}/rag", json=payload)
        response.raise_for_status()
        return response.json()
