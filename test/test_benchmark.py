import pytest
from ingollmbencheval.benchmark import is_correct_response


@pytest.mark.parametrize(
    "response, solution, match_type, expected",
    [
        # Exact-match tests
        ("hello world", "hello world", "exact-match", True),
        (" Hello World ", "hello world", "exact-match", False),
        ("hello world", "Hello World", "exact-match", False),
        ("ABC1", "abc1", "exact-match", False),
        ("ABC1", "ABC1", "exact-match", True),
        # Exact-match-ci tests
        ("hello world", "hello world", "exact-match-ci", True),
        (" Hello World ", "hello world", "exact-match-ci", True),
        ("hello world", "Hello World", "exact-match-ci", True),
        ("ABC1", "abc1", "exact-match-ci", True),
        ("ABC1", "ABC1", "exact-match-ci", True),
        # Partial-match tests
        ("Hello there, world!", "world", "partial-match", True),
        ("hello", "hell", "partial-match", True),
        ("hell", "hello", "partial-match", False),
        ("HELLO", "hello", "partial-match", True),
        # Regex-match tests
        ("abc123", r"abc\d{3}", "regex-match", True),
        ("abc124", r"abc\d{4}", "regex-match", False),
        (" abc123 ", r"abc\d{3}", "regex-match", True),
        ("abc123", r"^ABC\d{3}$", "regex-match", False),
        # Invalid regex pattern
        ("abc123", r"abc[", "regex-match", False),
        # Unknown match type
        ("response", "solution", "unknown-type", False),
    ],
)
def test_is_correct_response(response, solution, match_type, expected):
    assert is_correct_response(response, solution, match_type) == expected
