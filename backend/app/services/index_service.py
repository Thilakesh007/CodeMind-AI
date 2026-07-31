from app.parser.file_reader import read_repository
from app.parser.code_chunker import chunk_code
from app.embeddings.embedding_model import generate_embeddings
from app.vectorstore.chroma_client import store_chunks


def index_repository(
    project_name: str
):

    repo_path = f"../repositories/{project_name}"


    files = read_repository(
        repo_path
    )


    chunks = chunk_code(
        files,
        project_name
    )


    texts = [
        chunk["content"]
        for chunk in chunks
    ]


    embeddings = generate_embeddings(
        texts
    )


    store_chunks(
        chunks,
        embeddings
    )


    return {
        "success": True,
        "project": project_name,
        "files": len(files),
        "chunks": len(chunks)
    }
