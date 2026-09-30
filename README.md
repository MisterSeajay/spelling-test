# Spelling Test

## Overview

This **Python** program performs a spelling test. The words to be spelled are "spoken" and have to be typed in
correctly in lower-case, with capitals and other punctuation only as required.

## Requirements

### Git

There is no binary installer for this (very!) simple program. You need to download the necessary files from GitHub.
Since the easiest way to do this is with **Git** itself, installing the **Git** package is very useful.

- [Git Downloads](https://git-scm.com/downloads)

### Python 3

The program was written in Python v3 and is **not** compatible with Python v2. The pinned version is in
`.python-version`.

### uv

This project uses [uv](https://docs.astral.sh/uv/) for dependency and environment management:

~~~bash
uv sync
~~~

This creates a virtual environment and installs the project plus its dependencies.

## Download

This program is provided as a GitHub repo. It is expected that you will be able to download (clone) the necessary
files using **git**.

### Linux

The following commands will create a folder called **Git** in your home directory on Linux when run from a
terminal prompt:

~~~bash
cd ~
mkdir Git
cd Git
git clone https://github.com/MisterSeajay/spelling-test.git
~~~

## Running the spelling test

The `spelling-test` command is installed into the local environment by `uv sync`:

~~~bash
uv run spelling-test
~~~

Prompts and results are written to the terminal with **rich**, while log messages go to **stderr** with **loguru**.

### Options

| Option | Description |
| --- | --- |
| `--user`, `-u` | The name of the profile to use for the test. Prompted for if omitted. |
| `--level`, `-l` | The level (school year) to test at. Defaults to the profile's level. |
| `--test`, `-t` | The named list of words to be tested on. Defaults to `*`, meaning the level-based list. |
| `--questions`, `-q` | The number of words to test. Defaults to `10`. |
| `--json` | Emit machine-readable JSON instead of rich output. |
| `--verbose` | Show `INFO` level logs. |
| `--debug` | Show `DEBUG` level logs. |

### In-test commands

Typing `?show` instead of an answer reveals the current word and does not count as an attempt.

## Layout

- `src/spelling_test/` — the package
  - `main.py` — the `typer` CLI entry point
  - `user_profile.py` — per-user level and word scores, stored in `<user>.profile`
  - `dictionary_handler.py` — loading and querying `data/dictionary.json`
  - `audio_handler.py` — text-to-speech and playback
- `data/dictionary.json` — the word lists
- `mp3_cache/` — cached audio, filled on demand

## Development

### Code quality

- `ruff` for linting, configured in `pyproject.toml`
- `pyright` for type checking

~~~bash
uv run ruff check .
uv run pyright
~~~

### Documentation

Markdown files are linted with markdownlint-cli2 (npm package) and wrap at 120 characters.

## Gotchas

### Linux installation of gTTS

At the time of writing there seems to be a problem with the installation of the gTTS library, acknowledged in
[gTTS issue 158](https://github.com/pndurette/gTTS/issues/158#issuecomment-446411841) on GitHub. The work-around
suggested in that thread worked for me, although I had to update the path to reflect my version of Python 3.5:

~~~bash
cd ~/.local/lib/python3.5/site-packages/
mv UNKNOWN-2.0.3.dist-info/ gTTS-2.0.3.dist-info/
pip install --user --force-reinstall --ignore-installed --no-binary :all: gTTS
~~~
