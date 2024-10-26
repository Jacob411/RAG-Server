
import requests

url = "http://localhost:7272/v2/update_files"



# use test.txt

files = {
    'files': ('test.txt', open('test.txt', 'rb'), 'text/plain')  # Tuple format for file
}

# Make the POST request
response = requests.post(url, files=files)

# Check the response
print(response.status_code)
print(response.json())  # Print the response JSON if available

