import pytest

@pytest.fixture(autouse=True)
def mock_llm_calls(monkeypatch):
    """Mock all LLM API calls"""
    def mock_chat(*args, **kwargs):
        return ("mocked response", "")
    
    monkeypatch.setattr("llm_client.LLMClient.chat", mock_chat)