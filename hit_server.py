import json
import requests

BASE_URL = "http://localhost:7272"

def update_files():
    files = {
        'files': ('test.txt', open('test.txt', 'rb'), 'text/plain')  
    }

    url = f"{BASE_URL}/v2/ingest_files"
    response = requests.post(url, files=files)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()

def list_documents():

    url = f"{BASE_URL}/v2/documents_overview"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()


def delete_files():
    url = f"{BASE_URL}/v2/delete"
    document_id = "30f950f0-c692-57c5-b6ec-ff78ccf5ccdc"
    # Format filters as a JSON object with field name as the key directly
    filters = {
        "document_id": {
            "$eq": document_id
        }
    }
    params = {
        "filters": json.dumps(filters)  # Convert filters to JSON string
    }
    
    response = requests.delete(url, params=params)
    
    try:
        return response.json()
    except:
        return response.status_code


def rag(query):
    url = f"{BASE_URL}/v2/rag"
    query = {
        "query": query,

    }
    response = requests.post(url, data=json.dumps(query), headers={"Content-Type": "application/json"})
    
    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()

if __name__ == "__main__":
    results = list_documents()

    for result in results['results']:
        print(result['title'])

    
    query = "What is the capital of France?"
    results = rag(query)['results']['completion']
    print(json.dumps(results, indent=2))

