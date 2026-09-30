import json
import jsonpath
from pathlib import Path
from itertools import chain

DIC_PATH = Path("data/dictionary.json").absolute().as_posix()

def load_dictionary() -> dict:
    with open(DIC_PATH) as f:
        return json.load(f)

def get_word_help(dictionary: dict, help_type: str) -> dict:
    word_help = {}
    jsonpath_filter = f"$.dictionary[*].{help_type}"
    item_list = jsonpath.jsonpath(dictionary, jsonpath_filter)
    for item in item_list:
        word_help = dict(chain.from_iterable(word_help.items(), item.items()))
    return word_help

def get_random_words(level: int, name: str, questions: int, dictionary: dict, profile) -> list:
    word_list = set()
    while not word_list:
        if name == "*":
            jsonpath_filter = f"$.dictionary[?(@.level=={level} || @.level=={int(level)-1})].words"
        else:
            jsonpath_filter = f'$.dictionary[?(@.name == "{name}")].words'
        
        words = jsonpath.jsonpath(dictionary, jsonpath_filter)
        if not words:
            raise ValueError(f"No words found for query: {jsonpath_filter}")

        for sublist in words:
            for item in sublist:
                if item not in profile.words or profile.words[item] > -1:
                    word_list.add(item)
        
        if not word_list:
            level += 1
            
    return list(word_list[i] for i in random.sample(range(len(word_list)), min(len(word_list), questions)))
