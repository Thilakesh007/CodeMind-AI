from app.vectorstore.chroma_client import search_vectors
from app.ai.ai_client import generate_response
from app.ai.prompts import README_PROMPT

import json

def generate_readme(question: str, project: str = None, history: list = None, stream: bool = False):
    # Retrieve relevant context
    context_docs = search_vectors(question, project_name=project, n_results=5)
    
    # Format context
    context_text = "\n\n".join([doc["content"] for doc in context_docs])
    
    # Construct final prompt
    prompt = f"{README_PROMPT}\n\nContext:\n{context_text}\n\nTask: {question}"
    
    if stream:
        def stream_generator():
            yield json.dumps({"sources": context_docs}) + "\n"
            for chunk in generate_response(prompt, history=history, stream=True):
                yield json.dumps({"chunk": chunk}) + "\n"
        return stream_generator()
    else:
        answer = generate_response(prompt, history=history, stream=False)
        return {
            "answer": answer,
            "sources": context_docs
        }
