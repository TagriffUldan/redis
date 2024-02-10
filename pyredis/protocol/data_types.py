from dataclasses import dataclass
from typing import Any, Protocol, Optional

@dataclass
class RespDataType(Protocol):
    data: Any

    def encode(self) -> bytes:
        ...

@dataclass
class SimpleString:
    data: str

    def encode(self) -> bytes:
        return f"+{self.data}\r\n".encode()
    
@dataclass 
class SimpleError:
    data: str

    def encode(self) -> bytes:
        ...

@dataclass
class Integer:
    data: int

    def encode(self) -> bytes:
        ...    
    

@dataclass
class BulkString:
    data: Optional[str]

    def encode(self) -> bytes:
        ...

@dataclass
class Array:
    data: Optional[list[Optional[RespDataType]]]

    def __getitem__(self, i: int) -> Optional[RespDataType]:
        if self.data:
            return self.data[i]
        
    def __len__(self) -> Optional[int]:
        if self.data:
            return len(self.data)

    def encode(self) -> bytes:
        ...
    

@dataclass
class Nulls:
    data: None

    def encode(self) -> bytes:
        ...


def encode_message(message: RespDataType) -> bytes:
    return message.encode()