import re
from string import punctuation
import json
from typing import Dict, Callable, List
from functools import reduce


def load_txt(txt_path:str) -> str:
    """Loads a txt file."""
    with open(txt_path, 'r') as file:
        file_content = file.read()
    return file_content

def load_json(json_path:str) -> Dict:
    """Loads a json file."""
    with open(json_path) as file:
        data = json.load(file)
    return data  

def erase_diacritics(text:str):
    """Erases diacritical marks."""
    return text.translate(str.maketrans('áéíóúüÁÉÍÓÚÜàèìòùÀÈÌÒÙ','aeiouuAEIOUUaeiouAEIOU'))

def erase_punctuation(text:str):
    """Erases punctuation."""
    return re.sub(f"[{punctuation}'¿¡‘’]", '', text)

def process_string(text:str, fn_sequence:List) -> str:
    """Processes a string by applying a series of functions sequentially."""
    final_result = reduce(lambda x, func: func(x), fn_sequence, text)
    return final_result