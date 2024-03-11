from pyredis.protocol_handler import RespDataType, SimpleString, SimpleError, Integer, BulkString, Array
from pyredis.protocol_handler import extract_frame_from_buffer
from pyredis.protocol_handler import parse_simple_string, parse_simple_errors, parse_integers, parse_bulk_string, parse_array
import pytest

@pytest.mark.parametrize("buffer, expected", [
    (b"+Par", (None, 0)),
    (b"+OK\r\n", (SimpleString("OK"), 5)),
    (b"+OK\r\n+Next", (SimpleString("OK"), 5)),
    (b"-Error message\r\n", (SimpleError("Error message"), 16)),
    (b"$-1\r\n", (None, 0)),
    (b"*0", (None, 0)),
])
def test_read_frame_simple_string(buffer: bytes, expected: tuple[RespDataType | None, int]):
    actual_data_type, actual_length = extract_frame_from_buffer(buffer)
    expected_data_type, expected_length = expected
    assert actual_data_type == expected_data_type
    assert actual_length == expected_length


@pytest.mark.parametrize("buffer, separator_index, expected", [
    (b"+OK\r\n", 3, (SimpleString("OK"), 5)),
    (b"+appleshit\r\n", 10, (SimpleString("appleshit"), 12)),
])
def test_parse_simple_string(buffer: bytes, separator_index: int, expected: tuple[RespDataType | None, int]):
    actual_data_type, actual_length = parse_simple_string(buffer, separator_index)
    expected_data_type, expected_length = expected
    assert actual_data_type == expected_data_type
    assert actual_length == expected_length


@pytest.mark.parametrize("buffer, separator_index, expected", [
    (b"-Error message\r\n", 14, (SimpleError("Error message"), 16)),
])
def test_parse_simple_errors(buffer: bytes, separator_index: int, expected: tuple[RespDataType | None, int]):
    actual_data_type, actual_length = parse_simple_errors(buffer, separator_index)
    expected_data_type, expected_length = expected
    assert actual_data_type == expected_data_type
    assert actual_length == expected_length

@pytest.mark.parametrize("buffer, separator_index, expected", [
    (b":5\r\n", 2, (Integer(5), 4)),
    (b":-500\r\n", 5, (Integer(-500), 7)),
    (b":+10\r\n", 4, (Integer(10), 6)),
    (b":+100000\r\n", 8, (Integer(100000), 10)),
])
def test_parse_integers(buffer: bytes, separator_index: int, expected: tuple[RespDataType | None, int]):
    actual_data_type, actual_length = parse_integers(buffer, separator_index)
    expected_data_type, expected_length = expected
    assert actual_data_type == expected_data_type
    assert actual_length == expected_length


@pytest.mark.parametrize("buffer, separator_index, expected", [
    (b"$5\r\nhello\r\n", 2, (BulkString("hello"), 11)),
    (b"$-1\r\n", 3, (None, 0)),
    (b"$9\r\nintercept\r\n", 2, (BulkString("intercept"), 15)),
    (b"$9\r\nintercept\n\r", 2, (None, 0)),
    (b"$11\r\nintercepted\r\n", 3, (BulkString("intercepted"), 18))
])
def test_parse_bulk_string(buffer: bytes, separator_index: int, expected: tuple[RespDataType | None, int]):
    actual_data_type, actual_length = parse_bulk_string(buffer, separator_index)
    expected_data_type, expected_length = expected
    assert actual_data_type == expected_data_type
    assert actual_length == expected_length


@pytest.mark.parametrize("buffer, separator_index, expected", [
    (b"*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n", 2, (Array([BulkString("hello"), BulkString("world")]), 26)),
    (b"*0\r\n", 2, (Array([]), 4)),
    (b"*3\r\n:1\r\n:2\r\n:3\r\n", 2, (Array([Integer(1), Integer(2), Integer(3)]), 16)),
    (b"*2\r\n*3\r\n:1\r\n:2\r\n:3\r\n*2\r\n+Hello\r\n-World\r\n", 2, 
     (Array(data=[Array(data=[Integer(data=1), Integer(data=2), Integer(data=3)]), 
                  Array(data=[SimpleString(data='Hello'), SimpleError(data='World')])]), 40))
])
def test_parse_array(buffer: bytes, separator_index: int, expected: tuple[RespDataType | None, int]):
    actual_data_type, actual_length = parse_array(buffer, separator_index)
    expected_data_type, expected_length = expected
    assert actual_data_type == expected_data_type
    assert actual_length == expected_length