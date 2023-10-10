from langchain.prompts import PromptTemplate 
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from utils import load_txt
from config import GptConfig
import json
from typing import Callable, List

playlist_guidelines = ""

class GPTPlaylist:

    def __init__(
            self, 
            prompt_template:PromptTemplate=PromptTemplate, 
            llm:ChatOpenAI=ChatOpenAI, 
            chain:LLMChain=LLMChain,
            config:GptConfig=GptConfig
            ) -> None:
        
        self.config_secrets = config()
        self.config_parameters = config.load_json_parameters()
        self.input_guidelines = self.config_parameters["prompt_input_guidelines"]
        self.input_json_schema = self.config_parameters["prompt_input_json_schema"]
        self.prompt = load_txt(self.config_parameters["playlist_prompt_path"])
        self.playlist_name = load_txt(self.config_parameters["playlist_name_path"])
        self.prompt_template = prompt_template
        self.llm = llm
        self.chain = chain

    def _init_chain(
            self,
            template:str,
            input_variables:List
            ) -> Callable[[str], LLMChain]:
        """
        #TODO: Pasar acá todos los parámetros de inicialización relacionados al chain, quizás
        """
        prompt_template = self.prompt_template.from_template(            
            #input_variables=input_variables, #, self.input_json_schema
            template=template,
            template_format="jinja2"
        )
        llm = self.llm(
            temperature=self.config_parameters["temperature"], 
            model_name=self.config_parameters["model"], 
            openai_api_key=self.config_secrets.api_key
        )
        chain = self.chain(
            llm=llm, 
            prompt=prompt_template
        )
        return chain

    def generate_playlist(self, input_guideline):
        playlist = json.loads(
            self._init_chain(
            template=self.prompt, 
            input_variables=[self.input_guidelines, self.input_json_schema]
            ).run(
                {"guidelines":input_guideline, "json_schema":self.input_json_schema}
            )
            )
        return playlist


    def generate_playlist_name(self, input_guideline):
        name = self._init_chain(template=self.playlist_name, input_variables=[self.input_guidelines]).run({"guidelines:":input_guideline})
        return name





