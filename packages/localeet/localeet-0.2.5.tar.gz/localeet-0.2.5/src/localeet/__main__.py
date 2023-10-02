"""
Entry point for CLI. Define and parse CLI arguments.
"""
from os import environ as env
from pathlib import Path
from typing import Optional

import click

from localeet.get_leetcode_problem import run
from localeet.get_version import get_version
from localeet.language_maps import LANGUAGE_TO_EXTENSION


DIFFICULTY_MAP = {
    'easy': 1,
    'medium': 2,
    'hard': 3,
    '1': 1,
    '2': 2,
    '3': 3,
}

SUPPORTED_LANGUAGES = list(LANGUAGE_TO_EXTENSION.keys())


@click.command()
@click.option(
    '--max_difficulty', '--max',
    help='Max difficulty allowed',
    type=click.Choice(list(DIFFICULTY_MAP.keys())),
    default=env.get('LOCALEET_DEFAULT_MAX_DIFFICULTY', 'hard'),
)
@click.option(
    '--min_difficulty', '--min',
    help='Min difficulty allowed',
    type=click.Choice(list(DIFFICULTY_MAP.keys())),
    default=env.get('LOCALEET_DEFAULT_MIN_DIFFICULTY', 'easy'),
)
@click.option(
    '--output_path', '--path', '-o',
    help='Output path for code file. Will create new directories as needed.',
    default=env.get('LOCALEET_DEFAULT_OUTPUT_PATH', '.'),
)
@click.option(
    '--code_editor_open_command', '--editor', '-e',
    help='Will open the specified editor on the created file.',
    default=env.get('LOCALEET_DEFAULT_CODE_EDITOR_OPEN_COMMAND', 'code'),
)
@click.option(
    '--programming_language', '--language', '-l',
    help='The programming language you want to use for your output file',
    type=click.Choice(SUPPORTED_LANGUAGES),
    default=env.get('LOCALEET_DEFAULT_LANGUAGE', 'python3'),
)
@click.option(
    '--version', '-v',
    help='Print the current version of localeet',
    is_flag=True,
)
def main(
        max_difficulty: str,
        min_difficulty: str,
        output_path: str,
        code_editor_open_command: str,
        programming_language: str,
        version: bool,
    ) -> Optional[str]:
    """Entry point for CLI. Parse CLI arguments."""
    if version:
        return get_version()

    max_difficulty = DIFFICULTY_MAP.get(max_difficulty)
    min_difficulty = DIFFICULTY_MAP.get(min_difficulty)

    output_path = Path(output_path)

    language = programming_language.lower()
    if SUPPORTED_LANGUAGES.index(language) is None:
        msg = f'{programming_language} is not a supported languge'
        raise ValueError(msg)
    if language == 'python':
        language = 'python3'  # python2 is dead, long live python3
    elif language == 'go':
        language = 'golang'

    run(
        max_difficulty,
        min_difficulty,
        output_path,
        code_editor_open_command,
        language,
    )
    return None
