import protocol.protocol_handler as ph
from protocol.data_types import *

start = b"*2\r\n*3\r\n:1\r\n:2\r\n:3\r\n*2\r\n+Hello\r\n-World\r\n"

object, length = ph.extract_frame_from_buffer(start)

if object is not None:
    transformed = object.encode_message()
    print(start == transformed)


input = SimpleString("Hello")

print(encode_message(input))

print("+Hello\r\n".encode() == encode_message(input))