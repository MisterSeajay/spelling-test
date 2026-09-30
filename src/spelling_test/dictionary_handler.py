import json
import random
from pathlib import Path
from typing import Any

import jsonpath

DIC_PATH = Path("data/dictionary.json").absolute()


def load_dictionary() -> dict[str, Any]:
    with open(DIC_PATH, encoding="utf-8") as f:
        return json.load(f)


def get_word_help(dictionary: dict[str, Any], help_type: str) -> dict[str, str]:
    """Flatten the per-list ``help_type`` entries into a single word -> help mapping."""
    jsonpath_filter = f"$.dictionary[*].{help_type}"
    item_list = jsonpath.jsonpath(dictionary, jsonpath_filter)
    word_help: dict[str, str] = {}
    for item in item_list:
        word_help.update(item)
    return word_help


def get_random_words(
    level: int,
    name: str,
    questions: int,
    dictionary: dict[str, Any],
    profile: Any,
) -> list[str]:
    """Pick up to ``questions`` unseen words, easing up a level if a list is exhausted."""
    word_list: set[str] = set()
    while not word_list:
        if name == "*":
            jsonpath_filter = f"$.dictionary[?(@.level=={level} || @.level=={int(level) - 1})].words"
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

    return random.sample(sorted(word_list), min(len(word_list), questions))
