import pytest
from unittest.mock import patch, MagicMock

@patch("app.vectorstore.chroma_client.store_chunks")
def test_mock_embedding(mock_store):
    # This is a placeholder test to verify embedding logic is mockable
    mock_store.return_value = None
    chunks = [{"id": "1", "content": "mock chunk", "metadata": {}}]
    
    mock_store(chunks, [[0.1, 0.2, 0.3]])
    mock_store.assert_called_once()