from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MessageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ORDER: _ClassVar[MessageType]
    HEALTH: _ClassVar[MessageType]
    RESPONSE: _ClassVar[MessageType]
ORDER: MessageType
HEALTH: MessageType
RESPONSE: MessageType

class Request(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: int
    def __init__(self, type: _Optional[int] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["type", "code", "contents"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    type: int
    code: int
    contents: str
    def __init__(self, type: _Optional[int] = ..., code: _Optional[int] = ..., contents: _Optional[str] = ...) -> None: ...
