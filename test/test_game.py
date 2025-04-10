import pytest
from game import Game
from player import Player

@pytest.fixture
def sample_game():
    return Game([
        {"name": "P1", "model": "m1"},
        {"name": "P2", "model": "m2"}
    ])

def test_game_initialization(sample_game):
    assert len(sample_game.players) == 2
    assert sample_game.game_record is not None
    assert sample_game.deck == []

def test_handle_system_challenge(sample_game, mocker):
    mocker.patch.object(sample_game, 'check_other_players_no_cards', return_value=True)
    current_player = sample_game.players[0]
    current_player.hand = ["A", "B"]
    
    sample_game.handle_system_challenge(current_player)
    assert len(current_player.hand) == 0