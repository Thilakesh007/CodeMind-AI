import os
import ast
import re

def detect_language(filename):
    ext = os.path.splitext(filename)[1]
    languages = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".html": "html",
        ".css": "css",
        ".md": "markdown",
        ".txt": "text"
    }
    return languages.get(ext, "unknown")

def parse_python_chunks(content):
    chunks = []
    try:
        tree = ast.parse(content)
        lines = content.split('\n')
        
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start_line = node.lineno - 1
                end_line = node.end_lineno
                chunk_content = '\n'.join(lines[start_line:end_line])
                chunks.append({
                    "type": type(node).__name__,
                    "name": node.name,
                    "content": chunk_content
                })
        
        # Add remaining code as a single chunk if the file is small, or just fall back to character chunking for the rest
        if not chunks and len(content) < 5000:
            chunks.append({"type": "module", "name": "module", "content": content})
            
    except Exception as e:
        pass # Fallback to naive chunking if syntax error
    return chunks

def parse_js_chunks(content):
    chunks = []
    # Extremely basic regex to find functions and classes
    # For a robust solution, tree-sitter is needed, but this works for MVP
    pattern = r'((?:async\s+)?function\s+\w+\s*\(.*?\)\s*\{|class\s+\w+\s*\{)'
    matches = list(re.finditer(pattern, content))
    
    for i, match in enumerate(matches):
        start_idx = match.start()
        # Find matching closing brace
        open_braces = 0
        end_idx = start_idx
        found_open = False
        
        for j in range(start_idx, len(content)):
            if content[j] == '{':
                open_braces += 1
                found_open = True
            elif content[j] == '}':
                open_braces -= 1
            
            if found_open and open_braces == 0:
                end_idx = j + 1
                break
                
        if found_open and open_braces == 0:
            chunks.append({
                "type": "block",
                "name": "js_block",
                "content": content[start_idx:end_idx]
            })
            
    if not chunks and len(content) < 5000:
        chunks.append({"type": "module", "name": "module", "content": content})
        
    return chunks

def chunk_code(files, project_name, chunk_size=1000):
    chunks = []
    chunk_id = 0

    for file in files:
        content = file.get("content", "")
        filename = file.get("file", file.get("path", "")) # handle both 'file' and 'path' keys depending on reader
        language = detect_language(filename)
        
        file_chunks = []
        
        if language == "python":
            file_chunks = parse_python_chunks(content)
        elif language in ["javascript", "typescript"]:
            file_chunks = parse_js_chunks(content)
            
        # Fallback to standard chunking
        if not file_chunks:
            for i in range(0, len(content), chunk_size):
                file_chunks.append({
                    "type": "raw",
                    "name": "raw_chunk",
                    "content": content[i:i+chunk_size]
                })

        for c in file_chunks:
            chunk_id += 1
            chunks.append({
                "project": project_name,
                "file": filename,
                "language": language,
                "chunk_id": chunk_id,
                "type": c["type"],
                "name": c["name"],
                "content": f"File: {filename}\nType: {c['type']} {c['name']}\n\n{c['content']}"
            })

    return chunks