from dataclasses import dataclass
from typing import Any, Protocol, Optional

@dataclass
class RespDataType(Protocol):
    data: Any

    def encode_message(self) -> bytes:
        ...


@dataclass
class SimpleString:
    data: str

    def encode_message(self) -> bytes:
        return f"+{self.data}\r\n".encode()

    def to_str(self) -> str:
        return self.data
    
@dataclass 
class SimpleError:
    data: str

    def encode_message(self) -> bytes:
        return f"-{self.data}\r\n".encode()
    
    def to_str(self) -> str:
        return self.data

@dataclass
class Integer:
    data: int

    def encode_message(self) -> bytes:
        return f":{self.data}\r\n".encode()

    def to_str(self) -> str:
        return str(self.data)

@dataclass
class BulkString:
    data: str

    def encode_message(self) -> bytes:
        length = len(self.data)
        return f"${length}\r\n{self.data}\r\n".encode()

    def to_str(self) -> str:
        return self.data

@dataclass
class Array:
    data: list[RespDataType]

    def __getitem__(self, i: int) -> Optional[RespDataType]:
        if self.data:
            return self.data[i]
        
    def __len__(self) -> Optional[int]:
        if self.data:
            return len(self.data)

    def encode_message(self) -> bytes:
        length = len(self.data)
        message = f"*{length}\r\n"

        for i in range(length):
            message += encode_message(self.data[i]).decode()

        return message.encode()
    

    
def encode_message(message: RespDataType) -> bytes:
    return message.encode_message()



