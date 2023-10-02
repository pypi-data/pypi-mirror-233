"""
Module to get a random LeetCode question according to certain
parameters and then output a local Python file to work on
said question.
"""

import random
import re
import subprocess
import textwrap
from pathlib import Path
from typing import Literal

import requests
from bs4 import BeautifulSoup

from localeet.language_maps import (
    LANGUAGE_TO_COMMENT,
    LANGUAGE_TO_EXTENSION,
)


ROOT = 'https://leetcode.com'
API_URL = f'{ROOT}/api/problems/all/'
GQL_URL = f'{ROOT}/graphql'

SLUG_KEY = 'question__title_slug'


def query_all_questions() -> dict:
    """Query LeetCode API for index of all questions"""
    return requests.get(API_URL, timeout=5).json()['stat_status_pairs']


def choose_a_valid_question(
        questions: list[dict],
        max_difficulty: Literal[1, 2, 3],
        min_difficulty: Literal[1, 2, 3],
    ) -> dict:
    """Recurse until a valid question is found, return its slug"""
    choice = random.choice(questions)
    if any((
        choice['paid_only'],
        choice['difficulty']['level'] < min_difficulty,
        choice['difficulty']['level'] > max_difficulty,
        choice['stat'].get(SLUG_KEY) is None,
    )):
        return choose_a_valid_question(
            questions,
            max_difficulty,
            min_difficulty,
        )
    return choice['stat'][SLUG_KEY]


def get_question_data(question_slug: dict) -> dict:
    """Get all metadata available for question via GraphQL query"""
    return requests.post(GQL_URL, timeout=10, json={
        'operationName': 'questionData',
        'variables': {
            'titleSlug': question_slug,
        },
        'query': """query questionData($titleSlug: String!) {
                        question(titleSlug: $titleSlug) {
                            questionId
                            questionFrontendId
                            boundTopicId
                            title
                            titleSlug
                            content
                            translatedTitle
                            translatedContent
                            isPaidOnly
                            difficulty
                            likes
                            dislikes
                            isLiked
                            similarQuestions
                            contributors {
                                username
                                profileUrl
                                avatarUrl
                                __typename
                            }
                            langToValidPlayground
                            topicTags {
                                name
                                slug
                                translatedName
                                __typename
                            }
                            companyTagStats
                            codeSnippets {
                                lang
                                langSlug
                                code
                                __typename
                            }
                            stats
                            hints
                            solution {
                                id
                                canSeeDetail
                                __typename
                            }
                            status
                            sampleTestCase
                            metaData
                            judgerAvailable
                            judgeType
                            mysqlSchemas
                            enableRunCode
                            enableTestMode
                            envInfo
                            libraryUrl
                            __typename
                        }
                    }
                """,
    }).json()


def parse_question_details(question_data: dict) -> dict[str, str]:
    """Parse response from GraphQL down into data needed for output"""
    soup = BeautifulSoup(question_data['data']['question']['content'], 'lxml')
    for code_tag in soup.find_all('code'):
        code_tag.replace_with('`' + code_tag.text + '`')
    return {
        'code_snippets': question_data['data']['question']['codeSnippets'],
        'difficulty': question_data['data']['question']['difficulty'],
        'question_id': question_data['data']['question']['questionId'],
        'question': soup.get_text().replace('\u00A0', ' '),
        'test_case': question_data['data']['question']['sampleTestCase'],
        'title': question_data['data']['question']['title'],
    }


def output_code_file(
        output_path: Path,
        question_details: dict[str, str],
        language: str,
    ) -> str:
    """Take question details and output a python file shell"""
    difficulty, qid, question, snippets, test_case, title = (
        question_details['difficulty'],
        question_details['question_id'],
        question_details['question'],
        question_details['code_snippets'],
        question_details['test_case'],
        question_details['title'],
    )
    extension = LANGUAGE_TO_EXTENSION[language]
    oc = LANGUAGE_TO_COMMENT[language]['open_block']
    cc = LANGUAGE_TO_COMMENT[language]['close_block']
    lc = LANGUAGE_TO_COMMENT[language]['line']
    snippet = next(i for i in snippets if i['langSlug'] == language)['code']
    output_path.mkdir(parents=True, exist_ok=True)
    regex = r'[-\s]+'  # replace spaces and hyphens with underscores
    file_name = f'{re.sub(regex, "_", title.lower())}.{extension}'
    output_path = output_path / file_name
    header = f'{oc}\n{qid} - {difficulty} - {title}\n\n{question}\n{cc}\n\n'
    content = header + snippet + f'\n{lc} Example test case:\n'
    content += '\n'.join([f'{lc} {d}' for d in test_case.split('\n')])
    content += f'\n\n{lc} Suggestion to get started:'
    content += f'\n{lc} 1. write 5-10+ good test cases, including edge cases'
    content += f'\n{lc} 2. write code to take test cases and call the function'
    content = [c.rstrip() for c in content.split('\n')]
    wrapped_content = []
    for s in content:
        if not s.strip():
            wrapped_content.append('')
            continue
        wrapped_lines = textwrap.wrap(s, width=79)
        wrapped_content.extend(wrapped_lines)
    content = '\n'.join(wrapped_content) + '\n'
    with output_path.open('w') as f:
        f.write(content)
    return str(output_path)


def open_code_editor(command: str, file_path: str) -> None:
    subprocess.run([command, file_path])  # noqa: S603


def run(
        max_difficulty: Literal[1, 2, 3],
        min_difficulty: Literal[1, 2, 3],
        output_path: Path,
        code_editor_open_command: str,
        programming_language: str,
    ) -> None:
    all_questions = query_all_questions()
    question_slug = choose_a_valid_question(
        all_questions,
        max_difficulty,
        min_difficulty,
    )
    result = get_question_data(question_slug)
    question_details = parse_question_details(result)
    output_path = output_code_file(
        output_path,
        question_details,
        programming_language,
    )
    open_code_editor(code_editor_open_command, output_path)
