import os
import tempfile
import requests
import pytest
from typing import Dict, Any, Generator

from rag_client import RAGClient

class TestRAGClientIntegration:
    @pytest.fixture(scope="class")
    def base_url(self) -> str:
        """Return the base URL for the API"""
        return "http://localhost:8000"

    @pytest.fixture(scope="class")
    def client(self, base_url: str) -> RAGClient:
        """Create a RAGClient instance"""
        return RAGClient(base_url=base_url)

    @pytest.fixture(scope="function")
    def test_file(self) -> Generator[str, None, None]:
        """Create a temporary test file for document ingestion"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test document for RAG integration testing.")
            temp_path = f.name

        yield temp_path
        
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    @pytest.fixture(scope="function")
    def ingested_document(self, client: RAGClient, test_file: str) -> Generator[dict, None, None]:
        """Fixture to ingest a test document and clean it up after the test"""
        response = client.ingest_file(test_file)
        assert 'document_id' in response[0]['results'][0], "Document ingestion failed"
        document_id = response[0]['results'][0]['document_id']
        
        yield response
        
        # Cleanup: Delete the ingested document
        try:
            client.delete_document(document_id)
        except requests.exceptions.RequestException:
            pytest.fail(f"Failed to cleanup test document: {document_id}")

    def test_health_check(self, client: RAGClient):
        """Test the health check endpoint"""
        response = client.check_health()
        
        assert response['status'] == 'healthy'
        assert response['rag_server'] == 'connected'

    def test_ingest_file(self, client: RAGClient, test_file: str):
        """Test file ingestion"""
        response = client.ingest_file(test_file)
        document_id = response[0]['results'][0]['document_id']
        assert 'document_id' in response[0]['results'][0]
        
        # Cleanup
        client.delete_document(document_id)

    def test_list_documents(self, client: RAGClient, ingested_document: dict):
        """Test listing documents"""
        response = client.list_documents()
        
        assert 'results' in response
        assert isinstance(response['results'], list)
        
        # Verify our ingested document is in the list
        document_ids = [doc['id'] for doc in response['results']]
        assert ingested_document[0]['results'][0]['document_id'] in document_ids

    def test_delete_document(self, client: RAGClient, test_file: str):
        """Test document deletion"""
        # First ingest a document
        ingest_response = client.ingest_file(test_file)
        document_id = ingest_response[0]['results'][0]['document_id']
        
        # Delete the document
        delete_response = client.delete_document(document_id)
        print(delete_response)
        
        assert delete_response['success'] is True
        assert delete_response['status_code'] == 200
        
        # Verify the document is no longer in the list
        list_response = client.list_documents()
        document_ids = [doc['id'] for doc in list_response['results']]
        assert document_id not in document_ids

    def test_search_functionality(self, client: RAGClient, ingested_document: dict):
        """Test search functionality"""
        response = client.search("test document")
        
        assert 'results' in response
        assert isinstance(response['results'], dict)

    def test_rag_query(self, client: RAGClient, ingested_document: dict):
        """Test RAG query functionality"""
        response = client.rag_query("What is this document about?")
        
        assert 'results' in response
        assert isinstance(response['results']['completion']['choices'][0]['message']['content'], str)

    def test_ingest_invalid_file(self, client: RAGClient):
        """Test ingesting a non-existent file"""
        with pytest.raises(FileNotFoundError):
            client.ingest_file("nonexistent_file.txt")

    def test_delete_nonexistent_document(self, client: RAGClient):
        """Test deleting a non-existent document"""
        response = client.delete_document("nonexistent_id")
        
        assert response['success'] is True
        assert response['status_code'] == 200

    @pytest.mark.parametrize("invalid_url", [
        "http://nonexistent-server:8000",
        "http://localhost:9999",
    ])
    def test_connection_errors(self, invalid_url: str):
        """Test handling of connection errors"""
        client = RAGClient(base_url=invalid_url)
        
        with pytest.raises(requests.exceptions.RequestException):
            client.check_health()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])