from src.protocol.protocol_handler import RespDataType, SimpleString, SimpleError, Integer, BulkString, Array
from src.protocol.protocol_handler import extract_frame_from_buffer
from src.protocol.protocol_handler import parse_simple_string, parse_simple_errors, parse_integers, parse_bulk_string, parse_array
import pytest

@pytest.mark.parametrize("buffer, expected", [
    (b"+Par", None),
    (b"+OK\r\n", SimpleString("OK")),
    (b"+OK\r\n+Next", SimpleString("OK")),
    (b"-Error message\r\n", SimpleError("Error message")),
    (b"$-1\r\n", None)
])
def test_read_frame_simple_string(buffer: bytes, expected: tuple[RespDataType | None, int]):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected


@pytest.mark.parametrize("buffer, separator_index, expected_data_type", [
    (b"+OK\r\n", 3, SimpleString("OK")),
])
def test_parse_simple_string(buffer: bytes, separator_index: int, expected_data_type: RespDataType):
    actual_data_type = parse_simple_string(buffer, separator_index)
    assert actual_data_type == expected_data_type


@pytest.mark.parametrize("buffer, separator_index, expected_data_type", [
    (b"-Error message\r\n", 14, SimpleError("Error message")),
])
def test_parse_simple_errors(buffer: bytes, separator_index: int, expected_data_type: RespDataType):
    actual_data_type = parse_simple_errors(buffer, separator_index)
    assert actual_data_type == expected_data_type

@pytest.mark.parametrize("buffer, separator_index, expected_data_type", [
    (b":5\r\n", 2, Integer(5)),
    (b":-500\r\n", 5, Integer(-500)),
    (b":+10\r\n", 4, Integer(10)),
    (b":+100000\r\n", 8, Integer(100000)),
])
def test_parse_integers(buffer: bytes, separator_index: int, expected_data_type: RespDataType):
    actual_data_type = parse_integers(buffer, separator_index)
    assert actual_data_type == expected_data_type


@pytest.mark.parametrize("buffer, separator_index, expected_data_type", [
    (b"$5\r\nhello\r\n", 2, BulkString("hello")),
    (b"$-1\r\n", 3, None),
    (b"$9\r\nintercept\r\n", 2, BulkString("intercept")),
    (b"$9\r\nintercept\n\r", 2, None),
])
def test_parse_bulk_string(buffer: bytes, separator_index: int, expected_data_type: RespDataType):
    actual_data_type = parse_bulk_string(buffer, separator_index)
    assert actual_data_type == expected_data_type


@pytest.mark.parametrize("buffer, separator_index, expected_data_type", [
    (b"*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n", 2, Array(["hello", "world"])),
    (b"*0\r\n", 2, Array([])),
])
def test_parse_array(buffer: bytes, separator_index: int, expected_data_type: RespDataType):
    actual_data_type = parse_array(buffer, separator_index)
    assert actual_data_type == expected_data_type
