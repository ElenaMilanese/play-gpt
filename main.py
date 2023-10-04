from string import punctuation
from langchain.prompts import PromptTemplate 
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import json
import re


def erase_diacritics(text:str):
    """ Removes diacritical marks """
    return text.translate(str.maketrans('áéíóúüÁÉÍÓÚÜàèìòùÀÈÌÒÙ','aeiouuAEIOUUaeiouAEIOU'))

def remove_punctuation(text:str):
    """ Removes punctuation """
    return re.sub(f"[{punctuation}'¿¡‘’]", '', text)

if __name__ == '__main__':
    print("Bienvenide a PlayGPT!\n")

    elementos = input("¿Cómo te gustaría que fuera la playlist?: ")

    api_key = os.environ.get("OPENAI_API_KEY")

    summary_template = """
        Proponer 10 canciones para armar una lista de reproducción de spotify a partir de los elementos {elementos}. 
        Tienen que ser similares en cuanto al estilo y bastante conocidas. Responder de forma concisa pero amable. 
        Devolverlo en formato json con una key "nombre" para el nombre de la canción y una key "artista" para el nombre del artista. 
        Revisar que las canciones sean verdaderas. No incluir los "ft." de la canción en el nombre del artista. 
        No repetir canciones.
    """
    summary_prompt_template =  PromptTemplate(input_variables=["elementos"], template=summary_template)

    llm =  ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=api_key) 

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    playlist = json.loads(chain.run(elementos=elementos))
    for x in playlist["canciones"]:
        print(x["nombre"], "-", x["artista"]) 
    respuesta = input("¿Guardo la lista? [sí/no]").strip().lower()

    if respuesta == "si":

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

        llm_nombre =  ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=api_key) 
        name_template = """
            Escribir un nombre de lista de spotify de una, dos o tres palabras basada en este input {elementos} y siendo imaginativo. No ponerle comillas al nombre.
        """
        nombre_prompt_template =  PromptTemplate(input_variables=["elementos"], template=name_template)
        chain1 = LLMChain(llm=llm_nombre, prompt=nombre_prompt_template)
        nombre = chain1.run(elementos=elementos)

        user_id = sp.current_user()["id"]
        playlist = sp.user_playlist_create(user=user_id, name=nombre, public=False)

        sp.playlist_add_items(playlist_id=playlist["id"], items=songs_unique)
        print(f"Se creó la lista de reproducción {nombre}.")
