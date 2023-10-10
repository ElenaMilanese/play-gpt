from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from config import SpotifyConfig
from utils import process_string, erase_diacritics, erase_punctuation
from typing import Dict, List

class SpotifyPlaylistCreator:
        
    def __init__(
        self, 
        spotify_client_credentials:SpotifyClientCredentials=SpotifyClientCredentials, 
        spotify:Spotify=Spotify, 
        spotify_oauth:SpotifyOAuth=SpotifyOAuth,
        config:SpotifyConfig=SpotifyConfig
        ) -> None:
    
        self.config_secrets = config()
        self.config_parameters = config.load_json_parameters()
        self.spotify_client_credentials= spotify_client_credentials(
            client_id=self.config_secrets.client_id, 
            client_secret=self.config_secrets.client_secret
        )
        self.sp = spotify(
            auth_manager=spotify_oauth(
                client_id=self.config_secrets.client_id, 
                client_secret=self.config_secrets.client_secret,
                redirect_uri=self.config_parameters["redirect_uri"],
                show_dialog=self.config_parameters["show_dialog"],
                scope=self.config_parameters["scope"]
            )
        )
        
    def search_songs(self, songs:Dict[str, Dict[str, str]]) -> List:
        """Searches for the songs in Spotify."""
        song_list = []
        for song in songs["canciones"]:
            try:
                norm_name = process_string(song["nombre"], [erase_diacritics, erase_punctuation])
                norm_artist = process_string(song["artista"], [erase_diacritics, erase_punctuation])
                result = self.sp.search(q=f'track:{norm_name} artist:{norm_artist}', type='track')
                uri = result['tracks']['items'][0]['uri']
                song_list.append(uri)
            except Exception as e:
                result = self.sp.search(q=norm_name, type='track')
                uri = result['tracks']['items'][0]['uri']
                song_list.append(uri)
            except Exception as e:
                print(e, "\n")
                print(f'La canción {song["nombre"]} de {song["artista"]} no existe en spotify, quizás flashó gpt :P')
        songs_unique = list(set(song_list))
        return songs_unique


    def create_playlist(self, song_list:List[str], playlist_name:str):
        """Create a playlist in Spotify with a list of songs"""
        user_id = self.sp.current_user()["id"]
        playlist = self.sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
        playlist_id = self.sp.playlist_add_items(playlist_id=playlist["id"], items=song_list)
        print(f"Se creó la lista de reproducción {playlist_name}.")
        return playlist_id 
