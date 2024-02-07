from dataclasses import dataclass
from typing import Any, Protocol

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
class Nulls:
    data: None