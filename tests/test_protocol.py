from src.protocol.protocol_handler import RespDataType, SimpleString, SimpleError
from src.protocol.protocol_handler import extract_frame_from_buffer
from src.protocol.protocol_handler import parse_simple_string, parse_simple_errors
import pytest

@pytest.mark.parametrize("buffer, expected", [
    (b"+Par", (None, 0)),
    (b"+OK\r\n", (SimpleString("OK"), 5)),
    (b"+OK\r\n+Next", (SimpleString("OK"), 5)),
    (b"-Error message\r\n", (SimpleError("Error message"), 16)),
    (b"$-1\r\n", (None, 0))
])
def test_read_frame_simple_string(buffer: bytes, expected: tuple[RespDataType | None, int]):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected

@pytest.mark.parametrize("buffer, separator_index, expected_data_type, expected_length", [
    (b"+OK\r\n", 3, SimpleString("OK"), 5),
])
def test_parse_simple_string(buffer: bytes, separator_index: int, expected_data_type: RespDataType, expected_length: int):
    actual_data_type, actual_length = parse_simple_string(buffer, separator_index)
    assert actual_data_type == expected_data_type
    assert actual_length == expected_length

@pytest.mark.parametrize("buffer, separator_index, expected_data_type, expected_length", [
    (b"-Error message\r\n", 14, SimpleError("Error message"), 16),
])
def test_parse_simple_errors(buffer: bytes, separator_index: int, expected_data_type: RespDataType, expected_length: int):
    actual_data_type, actual_length = parse_simple_errors(buffer, separator_index)
    assert actual_data_type == expected_data_type
    assert actual_length == expected_length