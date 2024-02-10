import pytest
from pyredis.protocol.data_types import RespDataType, SimpleString, SimpleError, Integer, encode_message


@pytest.mark.parametrize("message, expected", [
    (SimpleString("appleshit"), b"+appleshit\r\n"),
    (SimpleError("ERROR"), b"-ERROR\r\n"),
    (Integer(-3323442), b":-3323442\r\n"),
])
def test_encode_message(message: RespDataType, expected: bytes):
    actual = encode_message(message)
    assert actual == expected
