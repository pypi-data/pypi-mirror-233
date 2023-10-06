import pytest

from profitpulse.ui.console import message


@pytest.mark.parametrize(
    "text,max_line_length,expected",
    [
        ("", 1, "\n\t> \n"),
        ("abc", 1, "\n\t> abc\n"),
        ("abc", 3, "\n\t> abc\n"),
        ("abc", 4, "\n\t> abc\n"),
        ("abc cde", 1, "\n\t> abc\n\t  cde\n"),
        ("abc cde", 4, "\n\t> abc\n\t  cde\n"),
        ("abc cde fgh", 7, "\n\t> abc cde\n\t  fgh\n"),
        ("abc cde fgh hij", 7, "\n\t> abc cde\n\t  fgh hij\n"),
    ],
)
def test_split_big_messages_into_multiple_lines(text, max_line_length, expected):
    got = message(text, max_line_length)

    assert got == expected  # nosec
