import pytest
from pyredis.protocol.data_types import RespDataType, SimpleString, SimpleError, BulkString, Integer, Array, encode_message


@pytest.mark.parametrize("message, expected", [
    (SimpleString("appleshit"), b"+appleshit\r\n"),
    (SimpleError("ERROR"), b"-ERROR\r\n"),
    (Integer(-3323442), b":-3323442\r\n"),
    (BulkString("hello"), b"$5\r\nhello\r\n"),
    (BulkString("intercepted"), b"$11\r\nintercepted\r\n"),
    (Array(data=[Array(data=[Integer(data=1), Integer(data=2), Integer(data=3)]), 
                  Array(data=[SimpleString(data='Hello'), SimpleError(data='World')])]), b"*2\r\n*3\r\n:1\r\n:2\r\n:3\r\n*2\r\n+Hello\r\n-World\r\n"),
    (Array(data=[Integer(1), Integer(2), Integer(3)]), b"*3\r\n:1\r\n:2\r\n:3\r\n"),
])
def test_encode_message(message: RespDataType, expected: bytes):
    actual = encode_message(message)
    assert actual == expected
