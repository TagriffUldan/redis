from .data_types import (RespDataType, SimpleError, Integer, SimpleString)
from typing import Callable

MSG_SEPARATOR = b"\r\n"
ParseFn = Callable[[bytes, int], tuple[RespDataType, int]]

def parse_simple_string(buffer: bytes, separator_index: int) -> tuple[SimpleString, int]:
    return SimpleString(buffer[1:separator_index].decode()), separator_index + 2

def parse_simple_errors(buffer: bytes, separator_index: int) -> tuple[SimpleError, int]:
    return SimpleError(buffer[1:separator_index].decode()), separator_index + 2

def parse_integers(buffer: bytes, separator_index: int) -> tuple[Integer, int]:
    ...

VALID_FIRST_BYTES: dict[str, ParseFn] = {
    '+': parse_simple_string,
    '-': parse_simple_errors,
    ':': parse_integers,
}


def extract_frame_from_buffer(buffer: bytes) -> tuple[RespDataType | None, int]:
    first_byte = chr(buffer[0])

    if first_byte in VALID_FIRST_BYTES.keys():
        separator_index = buffer.find(MSG_SEPARATOR)

        if separator_index != -1:
            return VALID_FIRST_BYTES[first_byte](buffer, separator_index)

    return None, 0

print(extract_frame_from_buffer(b"+OK\r\n+Next"))