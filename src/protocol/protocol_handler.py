from dataclasses import dataclass
from typing import Protocol, Any

MSG_SEPARATOR = b"\r\n"


def parse_simple_string():
    ..


VALID_FIRST_BYTES: dict[str, Any] = {
    '+': '',
    '-': ''
}

@dataclass
class RespDataType(Protocol):
    data: Any

@dataclass
class SimpleString:
    data: str

@dataclass 
class SimpleError:
    data: str

@dataclass
class Nulls:
    data: None

def extract_frame_from_buffer(buffer: bytes) -> tuple[RespDataType, int]:
    first_byte = chr(buffer[0])

    if first_byte in VALID_FIRST_BYTES.keys():
        separator = buffer.find(MSG_SEPARATOR)
        if separator != -1:
            return SimpleString(buffer[1:separator].decode()), separator + 2

    return Nulls(None), 0

print(extract_frame_from_buffer(b"+OK\r\n+Next"))