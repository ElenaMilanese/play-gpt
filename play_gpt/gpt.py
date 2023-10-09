from langchain.prompts import PromptTemplate 
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from utils import load_txt
from config import GptConfig
import json
from typing import Callable

playlist_guidelines = ""

class GPTPlaylist:

    def __init__(
            self, 
            prompt_template:PromptTemplate=PromptTemplate, 
            llm:ChatOpenAI=ChatOpenAI, 
            chain:LLMChain=LLMChain,
            config:GptConfig=GptConfig
            ) -> None:
        
        self.config = config()
#        self.input_variable = self.config.prompt_input_variable
        self.prompt = load_txt(self.config.prompt_path)
        self.playlist_name = load_txt(self.config.playlist_name_path)
        self.prompt_template = prompt_template
        self.llm = llm
        self.chain = chain

    def _init_chain(
            self,
            template:str
            ) -> Callable[[str], LLMChain]:
        """
        #TODO: Pasar acá todos los parámetros de inicialización relacionados al chain, quizás
        """
        prompt_template = self.prompt_template(            
            input_variables=[self.input_variable], 
            template=template
        )
        llm = self.llm(
            temperature=self.config.temperature, 
            model_name=self.config.model, 
            openai_api_key=self.config.api_key
        )
        chain = self.chain(
            llm=llm, 
            prompt=prompt_template
        )
        return chain

    def generate_playlist(self, input_guideline):
        playlist = json.loads(self._init_chain(self.prompt).run(input_guideline))
        return playlist


    def generate_playlist_name(self, input_guideline):
        name = self._init_chain(self.playlist_name).run(input_guideline)
        return name





