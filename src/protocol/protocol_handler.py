from .data_types import (RespDataType, SimpleError, Integer, BulkString, SimpleString, Array)
from typing import Callable, Optional

MSG_SEPARATOR = b"\r\n"
ParseFn = Callable[[bytes, int], Optional[RespDataType]]


def parse_simple_string(buffer: bytes, separator_index: int) -> SimpleString:
    return SimpleString(buffer[1:separator_index].decode())


def parse_simple_errors(buffer: bytes, separator_index: int) -> SimpleError:
    return SimpleError(buffer[1:separator_index].decode())


def parse_integers(buffer: bytes, separator_index: int) -> Integer:
    factor = chr(buffer[1])
    if factor == '+' or factor == '-':
        multiplier = -1 if factor == '-' else 1
        integer = int(buffer[2:separator_index].decode())
        return Integer(multiplier * integer)
    else:
        integer = int(buffer[1:separator_index].decode())
        return Integer(integer)


def parse_bulk_string(buffer: bytes, separator_index: int) -> Optional[BulkString]:
    if buffer[1:3].decode() == '-1':
        return None
    
    if buffer[2+separator_index:].find(MSG_SEPARATOR) == -1:
        return None

    length = int(chr(buffer[1]))
    content = buffer[2+separator_index:2+separator_index+length].decode()
    return BulkString(content)


def parse_array(buffer: bytes, separator_index: int) -> Optional[Array]:
    if chr(buffer[1]) == '0':
        return Array([])

    return None
    

VALID_FIRST_BYTES: dict[str, ParseFn] = {
    '+': parse_simple_string,
    '-': parse_simple_errors,
    ':': parse_integers,
    '$': parse_bulk_string,
    '*': parse_array
}


def extract_frame_from_buffer(buffer: bytes) -> RespDataType | None:
    first_byte = chr(buffer[0])

    if first_byte in VALID_FIRST_BYTES.keys():
        separator_index = buffer.find(MSG_SEPARATOR)

        if separator_index != -1:
            return VALID_FIRST_BYTES[first_byte](buffer, separator_index)

    return None


def main():
    print(extract_frame_from_buffer(b"$5\r\nhello\r\n"))


if __name__ == '__main__':
    main()