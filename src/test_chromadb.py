import chromadb

def test_chromadb_connection():
    # Create a client
    client = chromadb.Client()
    
    # Create a collection
    collection = client.create_collection(name="test_collection")
    
    # Add some documents
    collection.add(
        documents=["This is a test document", "This is another test document"],
        metadatas=[{"source": "test1"}, {"source": "test2"}],
        ids=["id1", "id2"]
    )
    
    # Query the collection
    results = collection.query(
        query_texts=["test document"],
        n_results=2
    )
    
    print("ChromaDB is working! Query results:")
    print(results)

if __name__ == "__main__":
    test_chromadb_connection()