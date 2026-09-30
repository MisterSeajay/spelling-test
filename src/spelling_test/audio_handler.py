import asyncio
import pathlib

import edge_tts
import pygame
from loguru import logger

MP3_PATH = pathlib.Path.cwd().joinpath("mp3_cache")
VOICE = "en-GB-SoniaNeural"


def init_audio() -> None:
    pygame.mixer.init()


def play_audio(file_path: str) -> None:
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


async def save_mp3_audio(phrase: str, file_path: pathlib.Path) -> None:
    await edge_tts.Communicate(phrase, VOICE).save(file_path.as_posix())


def get_mp3_audio(word: str) -> str:
    mp3_file = MP3_PATH.joinpath(f"{word}.mp3")
    if not mp3_file.exists():
        phrase = f"Please spell the word: {word}"
        try:
            asyncio.run(save_mp3_audio(phrase, mp3_file.absolute()))
        except Exception as e:
            logger.error(f"Error generating audio for {word!r}: {e}")
    return mp3_file.absolute().as_posix()
