from src.protocol import SimpleString, extract_frame_from_buffer

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