from datetime import date

import pytest
from manage_movies.utils.utils import format_date


@pytest.mark.parametrize(
    "input_str, expected, expected_exc",
    [
        ("2024-06-22", date(2024, 6, 22), None),
        (None, None, None),
        ("22-06-2024", None, ValueError),
        ("2024/06/22", None, ValueError),
        ("invalid", None, ValueError),
        ("2024-02-30", None, ValueError),
    ],
    ids=[
        "valid_date",
        "none",
        "wrong_format_hyphens",
        "wrong_format_slashes",
        "non_date_string",
        "invalid_date",
    ],
)
def test_format_date(input_str, expected, expected_exc):
    """Test format_date for various inputs"""
    if expected_exc:
        with pytest.raises(expected_exc):
            format_date(input_str)
    else:
        result = format_date(input_str)
        if expected is None:
            assert result is None
        else:
            assert result == expected
            assert isinstance(result, date)
