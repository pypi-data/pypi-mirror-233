import json
from pathlib import Path
from typing import Any

import pytest


class MockValue:
    """Allows any of a datatype to pass comparison within dictionary"""
    def __init__(
            self,
            name: str = 'MOCK_VALUE',
            data_type: type = None,
            validator: callable = None,
        ) -> None:
        self.name = name
        self.data_type = data_type
        self.validator = validator

    def __eq__(self, item: Any) -> bool:  # noqa: ANN401
        if (
            (self.data_type and not isinstance(item, self.data_type)) or
            (self.validator and not self.validator(item))
        ):
            return False
        return True

    def __ne__(self, item: Any) -> bool:  # noqa: ANN401
        return not self.__eq__(item)

    def __repr__(self) -> str:
        return f'<ANY_{self.name}>'


@pytest.fixture(scope='session')
def any_int() -> MockValue:
    return MockValue('INT', int)


@pytest.fixture(scope='session')
def any_str() -> MockValue:
    return MockValue('STR', str)


@pytest.fixture(scope='session')
def any_version() -> MockValue:
    parts_in_semantic_version = 3
    return MockValue(
        'VERSION_NUMBER',
        str,
        lambda x: len(x.split('.')) == parts_in_semantic_version,
    )


@pytest.fixture(scope='session')
def any_json_str() -> MockValue:
    return MockValue('JSON_STR', str, lambda x: json.loads(x))


@pytest.fixture(scope='session')
def two_sum_details_json() -> dict:
    with Path('tests/data/two_sum_details.json').open() as f:
        return json.load(f)


@pytest.fixture(scope='session')
def two_sum_essentials() -> dict:
    with Path('tests/data/two_sum_essentials.json').open() as f:
        return json.load(f)
