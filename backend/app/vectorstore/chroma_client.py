import chromadb


client = chromadb.PersistentClient(
    path="../vector_db"
)


collection = client.get_or_create_collection(
    name="codebase"
)



def store_chunks(
    chunks,
    embeddings
):

    ids=[]
    documents=[]
    metadata=[]


    for i, chunk in enumerate(chunks):

        ids.append(
            str(i)
        )

        documents.append(
            chunk["content"]
        )

        metadata.append(
            {
                "project": chunk["project"],
                "file": chunk["file"],
                "language": chunk["language"],
                "chunk_id": chunk["chunk_id"]
            }
        )


    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadata
    )


    return True


def search_vectors(query: str, project_name: str = None, n_results: int = 5):
    from app.embeddings.embedding_model import generate_embeddings
    
    query_embedding = generate_embeddings([query])[0]
    
    kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": n_results
    }
    
    if project_name:
        kwargs["where"] = {"project": project_name}
        
    results = collection.query(**kwargs)
    
    formatted_results = []
    if results and results['documents']:
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                "content": results['documents'][0][i],
                "metadata": results['metadatas'][0][i] if results['metadatas'] else {}
            })
            
    return formatted_results

def delete_project_vectors(project_name: str):
    try:
        collection.delete(where={"project": project_name})
        return True
    except Exception as e:
        print(f"Error deleting vectors for {project_name}: {e}")
        return False