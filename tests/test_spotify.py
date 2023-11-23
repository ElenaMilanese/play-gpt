import pytest
from unittest.mock import MagicMock
from play_gpt.spotify import SpotifyPlaylistCreator

@pytest.mark.parametrize("songs, expected")
def test_find_songs():
    spc_mock = MagicMock()
    spc_mock.add.return_value = 10
    spc = SpotifyPlaylistCreator()
         


