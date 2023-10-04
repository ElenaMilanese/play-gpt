from langchain.prompts import PromptTemplate 
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import os
from utils import load_txt
from config import Config
import json
from typing import Callable


api_key = os.environ.get("OPENAI_API_KEY")

playlist_guidelines = ""

class GPTPlaylist():

    def __init__(
            self, 
            config:Config, 
            prompt_template:PromptTemplate, 
            llm:ChatOpenAI, 
            chain:LLMChain
            ) -> None:
        
        self.config = config()
        self.input_variable = self.config.prompt_input_variable
        self.prompt = load_txt(self.config.prompt_path)
        self.playlist_name = load_txt(self.config.playlist_name_path)
        self.prompt_template = prompt_template
        self.llm = llm
        self.chain = chain

    def _init_chain(
            template:str
            ) -> Callable:
        """
        #TODO: Pasar acá todos los parámetros de inicialización relacionados al chain, quizás
        """
        prompt_template = self.prompt_template(            
            input_variables=[self.input_variable], 
            template=self.prompt
        )
        llm = self.llm(
            temperature=self.config.temperature, 
            model_name=self.config.model, 
            openai_api_key=self.config.api_key
        )
        chain = self.chain(
            llm=self.llm, 
            prompt=template
        )
        return chain

    def generate_playlist():
        playlist = json.loads(self._init_chain(self.prompt).run(self.input_variable))


    def generate_playlist_name():
        name = self._init_chain(self.playlist_name).run(self.input_variable)





