from dataclasses import dataclass
from typing import Any, Protocol, Optional

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
class Integer:
    data: int

@dataclass
class BulkString:
    data: Optional[str]

@dataclass
class Array:
    data: Optional[list[Optional[RespDataType]]]

    def __getitem__(self, i: int) -> Optional[RespDataType]:
        if self.data:
            return self.data[i]
        
    def __len__(self) -> Optional[int]:
        if self.data:
            return len(self.data)
    


@dataclass
class Nulls:
    data: None