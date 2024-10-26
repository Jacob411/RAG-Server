
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

with open("test.txt", "w") as file:
    file.write("John is a person that works at Google.")

client.ingest_files(file_paths=["test.txt"])

# Call RAG directly
rag_response = client.rag(
    query="Who is john",
    rag_generation_config={"model": "openai/gpt-4o-mini", "temperature": 0.0},
)
results = rag_response["results"]
print(f"Search Results:\n{results['search_results']}")
print(f"Completion:\n{results['completion']}")
