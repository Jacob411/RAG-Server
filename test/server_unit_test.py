import unittest
from unittest.mock import patch, mock_open
import requests
from requests.models import Response
from typing import Dict, Any

class RAGClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def ingest_file(self, file_path: str) -> Dict[str, Any]:
        """Ingest a file to the RAG server"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{self.base_url}/documents/ingest", files=files)
            return response.json()

    def list_documents(self) -> Dict[str, Any]:
        """Get list of all documents"""
        response = requests.get(f"{self.base_url}/documents")
        response.raise_for_status()
        return response.json()

    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a document by ID"""
        response = requests.delete(f"{self.base_url}/documents/{document_id}")
        return response.json()

    def check_health(self) -> Dict[str, Any]:
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

class TestRAGClient(unittest.TestCase):
    def setUp(self):
        self.client = RAGClient()

    @patch('requests.post')
    def test_ingest_file(self, mock_post):
        mock_response = Response()
        mock_response._content = b'{"status": "success"}'
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        with patch("builtins.open", mock_open(read_data="file content")):
            result = self.client.ingest_file("test.txt")
            self.assertEqual(result, {"status": "success"})
            mock_post.assert_called_once()

    @patch('requests.get')
    def test_list_documents(self, mock_get):
        mock_response = Response()
        mock_response._content = b'{"results": [{"id": "1", "title": "Document 1"}]}'
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.client.list_documents()
        self.assertEqual(result, {"results": [{"id": "1", "title": "Document 1"}]})
        mock_get.assert_called_once_with("http://localhost:8000/documents")

    @patch('requests.delete')
    def test_delete_document(self, mock_delete):
        mock_response = Response()
        mock_response._content = b'{"status": "deleted"}'
        mock_response.status_code = 200
        mock_delete.return_value = mock_response

        result = self.client.delete_document("1")
        self.assertEqual(result, {"status": "deleted"})
        mock_delete.assert_called_once_with("http://localhost:8000/documents/1")

    @patch('requests.get')
    def test_check_health(self, mock_get):
        mock_response = Response()
        mock_response._content = b'{"status": "healthy"}'
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.client.check_health()
        self.assertEqual(result, {"status": "healthy"})
        mock_get.assert_called_once_with("http://localhost:8000/health")

if __name__ == '__main__':
    unittest.main()
