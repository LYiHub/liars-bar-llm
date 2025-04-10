import pytest
import tempfile
import json
import os
from game_analyze import analyze_game_records

@pytest.fixture
def sample_game_data():
    return {
        "winner": "PlayerA",
        "rounds": [{
            "play_history": [{
                "player_name": "PlayerA",
                "next_player": "PlayerB",
                "was_challenged": True,
                "challenge_result": True
            }],
            "round_result": {
                "shooter_name": "PlayerA",
                "bullet_hit": True
            }
        }]
    }

def test_analysis_calculation(sample_game_data):
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "test.json"), 'w') as f:
            json.dump(sample_game_data, f)
        
        stats = analyze_game_records(tmpdir)
        assert stats['wins']['PlayerA'] == 1
        assert stats['shots_fired']['PlayerA'] == 1