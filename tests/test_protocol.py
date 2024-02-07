from src.protocol.protocol_handler import SimpleString
from src.protocol.protocol_handler import extract_frame_from_buffer
import pytest

def test_read_frame_simple_string_incomplete_frame():
    buffer = b"+Par"
    frame, frame_size = extract_frame_from_buffer(buffer)
    assert frame == None
    assert frame_size == 0

def test_read_frame_simple_string_complete_frame():
    buffer = b"+OK\r\n"
    frame, frame_size = extract_frame_from_buffer(buffer)
    assert frame == SimpleString("OK")
    assert frame_size == 5

def test_read_frame_simple_string_extra_data():
    buffer = b"+OK\r\n+Next"
    frame, frame_size = extract_frame_from_buffer(buffer)
    assert frame == SimpleString("OK")
    assert frame_size == 5

@pytest.mark.parametrize("buffer, expected", [
    (b"+Par", (None, 0)),
    (b"+OK\r\n", (SimpleString("OK"), 5)),
    (b"+OK\r\n+Next", (SimpleString("OK"), 5)),
])
def test_read_frame_simple_string(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected