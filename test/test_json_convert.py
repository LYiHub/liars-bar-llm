import pytest
import tempfile
import json
import os
from json_convert import process_game_records

@pytest.fixture
def sample_json_game():
    return {
        "game_id": "TEST123",
        "rounds": [{
            "target_card": "A",
            "play_history": [{
                "player_name": "P1",
                "played_cards": ["A"],
                "remaining_cards": []
            }]
        }]
    }

def test_json_conversion(sample_json_game):
    with tempfile.TemporaryDirectory() as input_dir, \
         tempfile.TemporaryDirectory() as output_dir:
         
        # Create test input
        input_path = os.path.join(input_dir, "test.json")
        with open(input_path, 'w') as f:
            json.dump(sample_json_game, f)
            
        process_game_records(input_dir, output_dir)
        
        # Verify output
        output_path = os.path.join(output_dir, "test.txt")
        assert os.path.exists(output_path)
        with open(output_path, 'r') as f:
            content = f.read()
            assert "游戏ID: TEST123" in content