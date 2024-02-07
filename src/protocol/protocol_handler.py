from dataclasses import dataclass
from enum import Enum


MSG_SEPARATOR = b"\r\n"

class FIRST_BYTE(Enum):
    PLUS = '+'

VALID_FIRST_BYTES = {
    '+': ''
}

@dataclass
class SimpleString:
    data: str


def extract_frame_from_buffer(buffer: bytes) -> tuple[SimpleString | None, int]:
    first_byte = chr(buffer[0])

    if first_byte in VALID_FIRST_BYTES.keys():
        separator = buffer.find(MSG_SEPARATOR)
        if separator != -1:
            return SimpleString(buffer[1:separator].decode()), separator + 2

    return None, 0

print(extract_frame_from_buffer(b"+OK\r\n+Next"))