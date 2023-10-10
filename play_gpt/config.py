from pydantic_settings import BaseSettings
from typing import List, Dict
import os
from dotenv import load_dotenv
from utils import load_json
from constants import DEFAULT_CONFIG

load_dotenv()

#ENV_FILE = os.getenv("ENV_FILE", ".env")

class GptConfig(BaseSettings):
    api_key: str = os.getenv("OPENAI_API_KEY")
    #prompt_input_variables: List | str
    #prompt_path: str
    #playlist_name_path: str
    #temperature: int
    #model: str
    
    def load_json_parameters() -> Dict:
        """ Loads a json with configurable parameters"""
        return load_json(DEFAULT_CONFIG)["gpt"]

class SpotifyConfig(BaseSettings):
    client_id: str = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret: str = os.getenv("SPOTIFY_CLIENT_SECRET")
    #redirect_uri: str
    #show_dialog: bool
    #scope: str
    
    def load_json_parameters() -> Dict:
        """ Loads a json with configurable parameters"""
        return load_json(DEFAULT_CONFIG)["spotify"]

#class GeneralConfig(BaseSettings):
#    gpt_config: GptConfig
#    spotify_config: SpotifyConfig