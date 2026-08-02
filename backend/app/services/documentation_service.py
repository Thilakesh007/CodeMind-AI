from app.ai.ai_client import generate_response
from app.ai.prompts import DOCS_PROMPT
from app.vectorstore.chroma_client import search_vectors


import json

def generate_documentation(question: str, project: str = None, history: list = None, stream: bool = False, model: str = None):
    results = search_vectors(question, project_name=project)

    context = "\n\n".join(
        [
            item["content"]
            for item in results
        ]
    )

    prompt = DOCS_PROMPT.format(
        context=context,
        question=question
    )

    if stream:
        def stream_generator():
            yield json.dumps({"sources": results}) + "\n"
            for chunk in generate_response(prompt, history=history, stream=True, model=model):
                yield json.dumps({"chunk": chunk}) + "\n"
        return stream_generator()
    else:
        answer = generate_response(prompt, history=history, stream=False, model=model)
        return {
            "answer": answer,
            "sources": results
        }
