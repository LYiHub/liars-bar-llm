import pytest
import json
from unittest.mock import Mock, patch
from player import Player

@pytest.fixture
def mock_player():
    player = Player("TestPlayer", "test-model")
    player.hand = ["A", "B", "C"]
    player.llm_client = Mock()
    return player

def test_choose_cards_to_play_valid_response(mock_player):
    mock_response = json.dumps({
        "played_cards": ["A"],
        "behavior": "保守出牌",
        "play_reason": "测试原因"
    })
    mock_player.llm_client.chat.return_value = (mock_response, "")
    
    result = mock_player.choose_cards_to_play("", "", "")
    assert "played_cards" in result
    assert set(result["played_cards"]).issubset(mock_player.hand)

def test_decide_challenge_retry_logic(mock_player):
    mock_player.llm_client.chat.side_effect = [
        ("invalid_response", ""),
        ('{"was_challenged": true, "challenge_reason": ""}', "")
    ]
    
    result, _ = mock_player.decide_challenge("", "", "", "", "")
    assert mock_player.llm_client.chat.call_count == 2
    assert result["was_challenged"] is True

def test_reflect_updates_opinions(mock_player):
    mock_player.llm_client.chat.return_value = ("新的印象分析", "")
    
    mock_player.reflect(
        ["OtherPlayer"],
        "Round Info",
        "Action Info",
        "Result Info"
    )
    
    assert "OtherPlayer" in mock_player.opinions