import requests
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

if __name__ == "__main__":
    # Example usage
    client = RAGClient()
    
    # Check health
    print("Checking API health...")
    health = client.check_health()
    print(f"Health status: {health}")
    
    # Upload a file
    print("\nUploading file...")
    result = client.ingest_file("test.txt")
    print(f"Upload result: {result}")
    
    # List documents
    print("\nListing documents...")
    documents = client.list_documents()
    for doc in documents['results']:
        print(f"Document: {doc['title']} ({doc['id']})")



    to_delete = input("Enter the document id to delete: ")
    # Delete a document
    print(f"\nDeleting document {to_delete}...")
    delete_result = client.delete_document(to_delete)
    print(f"Delete result: {delete_result}")

    # 
    # # Delete a document
    # if documents['results']:
    #     doc_id = documents['results'][0]['document_id']
    #     print(f"\nDeleting document {doc_id}...")
    #     delete_result = client.delete_document(doc_id)
    #     print(f"Delete result: {delete_result}")
