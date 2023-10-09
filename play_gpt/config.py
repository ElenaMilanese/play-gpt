from pydantic import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

#ENV_FILE = os.getenv("ENV_FILE", ".env")

class GptConfig(BaseSettings):
    api_key: str = os.getenv("OPENAI_API_KEY")
    prompt_input_variables: List | str
    prompt_path: str
    playlist_name_path: str
    temperature: int
    model: str

class SpotifyConfig(BaseSettings):
    client_id: os.getenv("SPOTIFY_CLIENT_ID")
    client_secret: os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri: str
    show_dialog: bool
    scope: str

#class GeneralConfig(BaseSettings):
#    gpt_config: GptConfig
#    spotify_config: SpotifyConfig