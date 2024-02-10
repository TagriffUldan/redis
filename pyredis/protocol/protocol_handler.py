from .data_types import (RespDataType, SimpleError, Integer, BulkString, SimpleString, Array)
from typing import Callable, Optional, Tuple

_MSG_SEPARATOR = b"\r\n"
_MSG_SEPARATOR_SIZE = len(_MSG_SEPARATOR)

ParseFn = Callable[[bytes, int], Tuple[Optional[RespDataType], int]]


def parse_simple_string(buffer: bytes, separator_index: int) -> Tuple[SimpleString, int]:
    return SimpleString(buffer[1:separator_index].decode()), separator_index + _MSG_SEPARATOR_SIZE


def parse_simple_errors(buffer: bytes, separator_index: int) -> Tuple[SimpleError, int]:
    return SimpleError(buffer[1:separator_index].decode()), separator_index + _MSG_SEPARATOR_SIZE


def parse_integers(buffer: bytes, separator_index: int) -> Tuple[Integer, int]:
    return Integer(int(buffer[1:separator_index].decode())), separator_index + _MSG_SEPARATOR_SIZE


def parse_bulk_string(buffer: bytes, separator_index: int) -> Tuple[Optional[BulkString], int]:
    length = int(buffer[1:separator_index].decode())

    # ensure the buffer is as long as length indicates
    if len(buffer) < separator_index + _MSG_SEPARATOR_SIZE + length + _MSG_SEPARATOR_SIZE:
        return None, 0
    
    # ensure there is a correct terminating separator
    if buffer[separator_index+_MSG_SEPARATOR_SIZE:].find(_MSG_SEPARATOR) == -1:
        return None, 0

    if length == -1:
        return BulkString(None), length + _MSG_SEPARATOR_SIZE
    
    content = buffer[separator_index+_MSG_SEPARATOR_SIZE:separator_index+length+_MSG_SEPARATOR_SIZE].decode()

    return BulkString(content), separator_index + _MSG_SEPARATOR_SIZE + length + _MSG_SEPARATOR_SIZE


def parse_array(buffer: bytes, separator_index: int) -> Tuple[Optional[Array], int]:
    payload = buffer[1:separator_index].decode()
    length = int(payload)

    if length == 0:
        return Array([]), separator_index + _MSG_SEPARATOR_SIZE
    
    if length == -1:
        return Array(None), separator_index + _MSG_SEPARATOR_SIZE
    
    arr: list[Optional[RespDataType]] = []

    for _ in range(length):
        next_item, length = extract_frame_from_buffer(buffer[separator_index + _MSG_SEPARATOR_SIZE:])

        if next_item and length:
            arr.append(next_item)
            separator_index += length   
        else:
            return None, 0

    return Array(arr), separator_index + _MSG_SEPARATOR_SIZE
    

VALID_FIRST_BYTES: dict[str, ParseFn] = {
    '+': parse_simple_string,
    '-': parse_simple_errors,
    ':': parse_integers,
    '$': parse_bulk_string,
    '*': parse_array
}


def extract_frame_from_buffer(buffer: bytes) -> Tuple[RespDataType | None, int]:
    separator_index = buffer.find(_MSG_SEPARATOR)
    first_byte = chr(buffer[0])

    if first_byte in VALID_FIRST_BYTES.keys() and separator_index != -1:
        return VALID_FIRST_BYTES[first_byte](buffer, separator_index)

    return None, 0


def main():
    print(parse_array(b"*2\r\n*3\r\n:1\r\n:2\r\n:3\r\n*2\r\n+Hello\r\n-World\r\n", 2))



if __name__ == '__main__':
    main()