from app.ai.ai_client import generate_response
from app.ai.prompts import SYSTEM_PROMPT
from app.vectorstore.chroma_client import search_vectors


import json

def chat_with_repository(question: str, project: str = None, history: list = None, stream: bool = False):

    # 1. Retrieve relevant code chunks
    results = search_vectors(question, project_name=project)


    context = "\n\n".join(
        [
            item["content"]
            for item in results
        ]
    )


    # 2. Create AI prompt
    prompt = SYSTEM_PROMPT.format(
        context=context,
        question=question
    )


    # 3. Ask Ollama
    if stream:
        def stream_generator():
            # First send sources
            yield json.dumps({"sources": results}) + "\n"
            
            # Then stream chunks
            for chunk in generate_response(prompt, history=history, stream=True):
                yield json.dumps({"chunk": chunk}) + "\n"
                
        return stream_generator()
    else:
        answer = generate_response(prompt, history=history, stream=False)
        return {
            "answer": answer,
            "sources": results
        }
