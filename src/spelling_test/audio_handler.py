import pathlib
import pygame
from gtts import gTTS

MP3_PATH = pathlib.Path.cwd().joinpath("mp3_cache")

def init_audio():
    pygame.mixer.init()

def play_audio(file_path: str):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def get_mp3_audio(word: str) -> str:
    mp3_file = MP3_PATH.joinpath(f"{word}.mp3")
    if not mp3_file.exists():
        phrase = f"Please spell the word: {word}"
        try:
            tts = gTTS(phrase, lang="en-gb")
            tts.save(mp3_file.absolute().as_posix())
        except Exception as e:
            print(f"Error generating audio: {e}")
    return mp3_file.absolute().as_posix()
