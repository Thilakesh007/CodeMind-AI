from app.ai.ai_client import generate_response
from app.ai.prompts import SYSTEM_PROMPT
from app.vectorstore.chroma_client import search_vectors


import json

import re
import os

def chat_with_repository(question: str, project: str = None, history: list = None, stream: bool = False, model: str = None):
    # Context windowing: keep last 8 messages
    if history and len(history) > 8:
        history = history[-8:]

    # Parse @mentions
    mentions = re.findall(r'@([a-zA-Z0-9_\-\.]+)', question)
    
    explicit_results = []
    if mentions and project:
        repo_path = os.path.join("../repositories", project)
        if os.path.exists(repo_path):
            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    if file in mentions:
                        try:
                            file_path = os.path.join(root, file)
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()
                            
                            # Add to explicit results
                            explicit_results.append({
                                "content": f"// [EXPLICITLY MENTIONED FILE: {file}]\n{content}",
                                "metadata": {"file": file, "project": project}
                            })
                        except Exception as e:
                            print(f"Error reading mentioned file {file}: {e}")

    # 1. Retrieve relevant code chunks
    vector_results = search_vectors(question, project_name=project)
    
    # Combine results, prioritizing explicit mentions
    results = explicit_results + vector_results

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
            for chunk in generate_response(prompt, history=history, stream=True, model=model):
                yield json.dumps({"chunk": chunk}) + "\n"
                
        return stream_generator()
    else:
        answer = generate_response(prompt, history=history, stream=False, model=model)
        return {
            "answer": answer,
            "sources": results
        }
