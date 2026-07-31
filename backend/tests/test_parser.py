import pytest
from app.parser.code_chunker import chunk_code

def test_chunk_code_empty():
    files = []
    chunks = chunk_code(files, "emptyRepo")
    assert len(chunks) == 0

def test_chunk_code_valid():
    files = [
        {"path": "test.py", "content": "def hello():\n    print('world')"}
    ]
    chunks = chunk_code(files, "testRepo")
    assert len(chunks) > 0
    assert chunks[0]["file_path"] == "test.py"
    assert "def hello():" in chunks[0]["content"]