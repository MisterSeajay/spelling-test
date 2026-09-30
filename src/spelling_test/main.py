import json
import re
import sys
from pathlib import Path
from typing import Any

import typer
from loguru import logger
from rich.console import Console

from .audio_handler import get_mp3_audio, init_audio, play_audio
from .dictionary_handler import get_random_words, get_word_help, load_dictionary
from .user_profile import Profile

MP3_PATH = Path.cwd().joinpath("mp3_cache")

cli = typer.Typer(
    name="spelling-test",
    help="A simple spelling test!",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


def configure_logging(verbose: bool, debug: bool) -> None:
    """Loguru writes to stderr; default level is SUCCESS, raised by the CLI switches."""
    level = "DEBUG" if debug else "INFO" if verbose else "SUCCESS"
    logger.remove()
    logger.add(sys.stderr, level=level, format="<level>{level: <8}</level> {message}")


def get_user_profile(user: str) -> Profile:
    user_profile = Profile(user)
    if user_profile.profile_file_exists():
        user_profile.load_profile()
    return user_profile


def create_path(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def ask(question: str) -> str:
    """Prompt on stderr so piped stdout stays clean for `--json`."""
    return console.input(f"[bold]{question}[/bold]")


@cli.command()
def test(
    user: str = typer.Option(None, "--user", "-u", help="The name of the profile to use for the test"),
    level: int = typer.Option(None, "--level", "-l", help="The level (school year) to test at"),
    list_name: str = typer.Option("*", "--test", "-t", help="The named list of words to be tested on"),
    questions: int = typer.Option(10, "--questions", "-q", help="The number of words to test (default 10)"),
    as_json: bool = typer.Option(False, "--json", help="Emit machine-readable JSON instead of rich output"),
    verbose: bool = typer.Option(False, "--verbose", help="Show INFO level logs"),
    debug: bool = typer.Option(False, "--debug", help="Show DEBUG level logs"),
) -> None:
    """Run a spelling test."""
    configure_logging(verbose, debug)

    create_path(MP3_PATH)
    dictionary = load_dictionary()
    definitions = get_word_help(dictionary, "definitions")
    examples = get_word_help(dictionary, "examples")

    if not user:
        user = ask("Please enter your name: ")

    profile = get_user_profile(user.lower())

    if not level:
        level = profile.level

    words = get_random_words(level, list_name, questions, dictionary, profile)
    logger.info(f"Selected {len(words)} words for {profile.display_name} at level {level}")

    if list_name == "*":
        greeting = f"Today's test will be {len(words)} questions at level {level}"
    else:
        greeting = f"Today's test will be {len(words)} questions from the {list_name} list(s)"

    if not as_json:
        console.print(f"Hello, {profile.display_name}. {greeting}")

    count = 0
    init_audio()

    for count, word in enumerate(words, start=1):
        if word not in profile.words:
            profile.words[word] = 0

        mp3_file = get_mp3_audio(word)
        logger.debug(f"Question {count}/{len(words)}: {word!r} ({mp3_file})")

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

            attempt = ask(question)

            if attempt == "?show":
                console.print(word)

        profile.words[word] = profile.words[word] + (attempts - 2)

    results: dict[str, Any] = {
        "user": profile.display_name,
        "level": level,
        "questions": len(words),
        "words": [{"word": word, "score": profile.words[word]} for word in words],
    }

    if as_json:
        print(json.dumps(results))
    else:
        console.print("\n[bold green]Well done, you've completed the test![/bold green]\n")
        for word in words:
            console.print(f"Word: {word}, score {profile.words[word]:02d}")

    profile.save_profile()
    logger.info(f"Saved profile to {profile.profile_path}")


if __name__ == "__main__":
    cli()
