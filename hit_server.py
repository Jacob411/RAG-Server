import json
import requests

BASE_URL = "http://localhost:7272"

def update_files():
    files = {
        'files': ('test.txt', open('test.txt', 'rb'), 'text/plain')  
    }

    url = f"{BASE_URL}/v2/ingest_files"
    response = requests.post(url, files=files)

    print(response.status_code)
    print(response.json())
    return response.json()





def delete_files():
    url = f"{BASE_URL}/v2/delete"
    
    # Format filters as a JSON object with field name as the key directly
    filters = {
        "document_id": {"operator": "30f950f0-c692-57c5-b6ec-ff78ccf5ccdc", "value": "30f950f0-c692-57c5-b6ec-ff78ccf5ccdc"}
    }
    
    params = {
        "filters": json.dumps(filters)  # Convert filters to JSON string
    }
    
    response = requests.delete(url, params=params)

    print(response.status_code)
    print(response.json())
    return response.json()

if __name__ == "__main__":
    delete_files()


