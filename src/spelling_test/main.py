#!/usr/bin/python3
import argparse
import pathlib
import re
import random
from profile import Profile
from audio_handler import init_audio, get_mp3_audio, play_audio
from dictionary_handler import load_dictionary, get_word_help, get_random_words

MP3_PATH = pathlib.Path.cwd().joinpath("mp3_cache")
DIC_PATH = pathlib.Path.cwd().joinpath("data/dictionary.json").absolute().as_posix()

def get_user_profile(user: str) -> Profile:
    user_profile = Profile(user)
    if user_profile.profile_file_exists():
        user_profile.load_profile()
    return user_profile

def main(user: str = None, list_level: int = None, list_name: str = "*", questions: int = 10):
    create_path(MP3_PATH)
    dictionary = load_dictionary()
    definitions = get_word_help(dictionary, "definitions")
    examples = get_word_help(dictionary, "examples")

    if not user:
        user = input("Please enter your name: ")

    profile = get_user_profile(str.lower(user))

    if not list_level:
        list_level = profile.level

    words = list(
        get_random_words(list_level, list_name, questions, dictionary, profile)
    )

    if list_name == "*":
        print(f"Hello, {profile.display_name}. Today's test will be {len(words)} questions at level {list_level}")
    else:
        print(f"Hello, {profile.display_name}. Today's test will be {len(words)} questions from the {list_name} list(s)")

    count = 0
    init_audio()

    for word in words:
        if word not in profile.words:
            profile.words[word] = 0

        count += 1
        mp3_file = get_mp3_audio(word)

        attempts = 0
        attempt = ""
        while attempt != word:
            if not re.match(r"^\?", attempt):
                attempts += 1
            play_audio(mp3_file)
            question = f"Word {count:02d}, attempt {attempts:02d}: "

            if word in definitions:
                question += f'\nDefinition is "{definitions[word]}": '

            if word in examples:
                question += f'\nExample is "{examples[word]}": '

            attempt = input(question)

            if attempt == "?show":
                print(word)

        profile.words[word] = profile.words[word] + (attempts - 2)

    print("Well done, you've completed the test!\n")

    for word in words:
        print(f"Word: {word}, score {profile.words[word]:02d}")

    profile.save_profile()

def create_path(path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple spelling test!")
    parser.add_argument("--user", help="The name of the profile to use for the test")
    parser.add_argument("--level", help="The level (school year) to test at", dest="list_level", type=int)
    parser.add_argument("--test", help="The named list of words you want to be tested on", default="*", dest="list_name")
    parser.add_argument("--questions", help="The number of words to test (Default 10)", default=10, type=int)
    args = parser.parse_args()

    main(user=args.user, list_level=args.list_level, list_name=args.list_name, questions=args.questions)
