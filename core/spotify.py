from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from config import SpotifyConfig
from utils import process_string, erase_diacritics, erase_punctuation
from typing import Dict, List




client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://example.com"

class SpotifyPlaylist:
        
    def __init__(
        self, 
        config:SpotifyConfig, 
        spotify_client_credentials:SpotifyClientCredentials, 
        spotify:Spotify, 
        spotify_oauth:SpotifyOAuth
        ) -> None:
    
        self.config = config()
        self.spotify_client_credentials= spotify_client_credentials(
            client_id=self.config.client_id, 
            client_secret=self.config.client_secret
        )
        self.sp = spotify(
            auth_manager=spotify_oauth(
                client_id=self.config.client_id, 
                client_secret=self.config.client_secret,
                redirect_uri=self.config.redirect_uri,
                show_dialog=self.config.show_dialog,
                scope=self.config.scope
            )
        )
        
    def _search_songs(songs:Dict[str, Dict[str, str]]) -> List:
        """Searches for the songs in Spotify"""
        songs_list = []
        for song in songs["canciones"]:
            try:
                norm_name = process_string(song["nombre"], [erase_diacritics, erase_punctuation])
                norm_artist = remove_punctuation(remove_diacritics(song["artista"]))
                result = sp.search(q=f'track:{norm_name} artist:{norm_artist}', type='track')
                uri = result['tracks']['items'][0]['uri']
                songs.append(uri)
            except:
                print(f'La canción {song["nombre"]} de {song["artista"]} no existe en spotify, quizás flashó gpt :P')
        songs_unique = list(set(songs))


    def create_playlist():
        user_id = sp.current_user()["id"]
        playlist = sp.user_playlist_create(user=user_id, name=nombre, public=False)

        sp.playlist_add_items(playlist_id=playlist["id"], items=songs_unique)
        print(f"Se creó la lista de reproducción {nombre}.")
