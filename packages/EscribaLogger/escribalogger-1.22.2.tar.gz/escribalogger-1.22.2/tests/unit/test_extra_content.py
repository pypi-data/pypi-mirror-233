import pytest

from EscribaLogger.process_extra_context import process_extra_context


@pytest.mark.parametrize(
    "extra, expected",
    [
        (None, ""),
        ({"item": "value"}, r' - {"item": "value"}'),
    ],
)
def test_extra_context_processing_return_right_value(extra, expected):
    assert process_extra_context(extra) == expected


def test_extra_context_processing_raises_type_error_for_non_dict_parameters():
    with pytest.raises(TypeError):
        process_extra_context("some bad string")
