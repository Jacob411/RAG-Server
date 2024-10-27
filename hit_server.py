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
    

    return response.json()

if __name__ == "__main__":
    update_files()
    results = list_documents()

    for result in results['results']:
        print(result['title'])


