from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ["device", "on", "value"]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    ON_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    device: int
    on: bool
    value: int
    def __init__(self, device: _Optional[int] = ..., on: bool = ..., value: _Optional[int] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["requests"]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[Request]
    def __init__(self, requests: _Optional[_Iterable[_Union[Request, _Mapping]]] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ["on"]
    ON_FIELD_NUMBER: _ClassVar[int]
    on: bool
    def __init__(self, on: bool = ...) -> None: ...

class Vazio(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
