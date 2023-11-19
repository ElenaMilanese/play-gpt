from pydantic_settings import BaseSettings
from typing import List, Dict
import os
from utils import load_json
from constants import DEFAULT_CONFIG

config = load_json(DEFAULT_CONFIG)

class GptConfig(BaseSettings):
    api_key: str = os.getenv("OPENAI_API_KEY")
    prompt_input_guidelines: List | str = config["gpt"]["prompt_input_guidelines"]
    prompt_input_json_schema: str = config["gpt"][ "prompt_input_json_schema"]
    json_schema: str = config["gpt"][ "json_schema"]
    playlist_prompt_path: str = config["gpt"][ "playlist_prompt_path"]
    playlist_name_path: str = config["gpt"][ "playlist_name_path"]
    temperature: float = config["gpt"][ "temperature"]
    model: str = config["gpt"][ "model"]
    
    
class SpotifyConfig(BaseSettings):
    client_id: str = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret: str = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri: str = config["spotify"][ "redirect_uri"]
    show_dialog: bool = config["spotify"][ "show_dialog"]
    scope: str = config["spotify"][ "scope"]
