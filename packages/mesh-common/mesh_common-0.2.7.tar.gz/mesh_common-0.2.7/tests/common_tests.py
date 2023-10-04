from datetime import date, datetime
from typing import Optional, Union
from uuid import uuid4

import pytest

from mesh_common import is_optional, optional_origin_type
from mesh_common.text import Colors, Modifiers, colored_text


class _TestClass:
    pass


@pytest.mark.parametrize(
    ("test_type", "expected"),
    [
        (int, False),
        (bool, False),
        (str, False),
        (bytes, False),
        (datetime, False),
        (date, False),
        (_TestClass, False),
        (Union[None, int], True),  # noqa: UP007
        (Union[None, bool], True),  # noqa: UP007
        (Optional[int], True),  # noqa: UP007
        (Optional[bool], True),  # noqa: UP007
        (int | None, True),
        (bool | None, True),
        (Union[int, None], True),  # noqa: UP007
        (Union[_TestClass, None], True),  # noqa: UP007
        (Union[int, None, str], False),  # noqa: UP007
        (Union[_TestClass, None, int], False),  # noqa: UP007
        (Union[int, str], False),  # noqa: UP007
        (Union[int, int], False),  # noqa: UP007
    ],
)
def test_is_optional(test_type: type, expected: bool):
    assert is_optional(test_type) == expected, repr(test_type)


@pytest.mark.parametrize(
    ("test_type", "expected"),
    [
        (int, int),
        (_TestClass, _TestClass),
        (Union[None, int], int),  # noqa: UP007
        (Union[None, bool], bool),  # noqa: UP007
        (Optional[int], int),  # noqa: UP007
        (Optional[bool], bool),  # noqa: UP007
        (int | None, int),
        (bool | None, bool),
        (Union[int, None], int),  # noqa: UP007
        (Union[_TestClass, None], _TestClass),  # noqa: UP007
        (Union[int, None, str], Union[int, None, str]),  # noqa: UP007
        (Union[_TestClass, None, int], Union[_TestClass, None, int]),  # noqa: UP007
        (Union[int, str], Union[int, str]),  # noqa: UP007
        (Union[int, int], Union[int, int]),  # noqa: UP007
        (Union[int, int, None], int),  # noqa: UP007
    ],
)
def test_get_optional_origin_type(test_type: type, expected: type):
    assert optional_origin_type(test_type) == expected, repr(test_type)


def test_get_color_text():
    text = uuid4().hex
    red_text = colored_text(text, Colors.red)
    assert red_text == f"\033[31m{text}\033[0m"


def test_get_bold_green_flashing_text():
    text = uuid4().hex
    red_text = colored_text(text, Colors.green, Modifiers.bold, Modifiers.flash)
    assert red_text == f"\033[32;1;5m{text}\033[0m"


def test_get_bold_text():
    text = uuid4().hex
    red_text = colored_text(text, Colors.red, Modifiers.bold)
    assert red_text == f"\033[31;1m{text}\033[0m"


def test_get_bold_italic_text():
    text = uuid4().hex
    red_text = colored_text(text, Colors.red, Modifiers.bold, Modifiers.italic)
    assert red_text == f"\033[31;1;3m{text}\033[0m"
