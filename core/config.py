from pydantic import BaseSettings
from typing import List
import os

ENV_FILE = os.getenv("ENV_FILE", ".env")

class GptConfig(BaseSettings):
    prompt_input_variables: List | str
    prompt_path: str
    playlist_name_path: str
    temperature: int
    model: str
    api_key: str

class SpotifyConfig(BaseSettings):
    prompt_input_variables: List | str
    prompt_path: str
    playlist_name_path: str
    temperature: int
    model: str
    api_key: str

class GeneralConfig(BaseSettings):
    gpt_config: GptConfig
    spotify_config: SpotifyConfig