import pytest
from unittest.mock import MagicMock
from play_gpt.gpt import GPTPlaylist


@pytest.mark.parametrize("input_guideline, expected", [
    ("Una lista de canciones divertidas", "Fun Playlist"),
    ("Una lista de canciones tristes", "Sad Playlist")
])
def test_generate_playlist_name(input_guideline, expected):
    gpt_mock = MagicMock()
    gpt_mock._init_chain.return_value = expected
    gpt = GPTPlaylist()
    gpt._init_chain =  gpt_mock._init_chain
    assert gpt.generate_playlist_name(input_guideline) == expected
         
