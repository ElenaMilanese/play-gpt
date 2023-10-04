import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from utils import erase_diacritics, erase_punctuation


client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://example.com"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                        client_secret=client_secret,
                                        redirect_uri=redirect_uri,
                                        show_dialog=True,
                                        scope="playlist-modify-private"))

songs = []
for song in playlist["canciones"]:
    try:
        norm_name = remove_punctuation(remove_diacritics(song["nombre"]))
        norm_artist = remove_punctuation(remove_diacritics(song["artista"]))
        result = sp.search(q=f'track:{norm_name} artist:{norm_artist}', type='track')
        uri = result['tracks']['items'][0]['uri']
        songs.append(uri)
    except:
        print(f'La canción {song["nombre"]} de {song["artista"]} no existe en spotify, quizás flashó gpt :P')
songs_unique = list(set(songs))

user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id, name=nombre, public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=songs_unique)
print(f"Se creó la lista de reproducción {nombre}.")

songs = []
for song in playlist["canciones"]:
    try:
        norm_name = remove_punctuation(remove_diacritics(song["nombre"]))
        norm_artist = remove_punctuation(remove_diacritics(song["artista"]))
        result = sp.search(q=f'track:{norm_name} artist:{norm_artist}', type='track')
        uri = result['tracks']['items'][0]['uri']
        songs.append(uri)
    except:
        print(f'La canción {song["nombre"]} de {song["artista"]} no existe en spotify, quizás flashó gpt :P')
songs_unique = list(set(songs))

user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id, name=nombre, public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=songs_unique)