import datetime
from enum import Enum
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Mapping,
    Protocol,
    Type,
    TypeVar,
    runtime_checkable,
)

from . import rfc3339 as _rfc3339

T = TypeVar("T")


@runtime_checkable
class JsonSchemaCompatible(Protocol):
    def to_json(self) -> Dict[str, Any]:
        ...

    @classmethod
    def from_json(cls: Type[T], data: Mapping[str, Any]) -> T:
        ...


class Serialisation(Protocol):
    def serialise(self, value: Any) -> Any:
        ...

    def deserialise(self, value: Any) -> Any:
        ...

    def as_list(self) -> "ListOf":
        return ListOf(self)

    def as_map(self) -> "MapOf":
        return MapOf(self)


class ListOf(Serialisation):
    def __init__(self, serialisation: Serialisation) -> None:
        self.serialisation = serialisation

    def serialise(self, value: List[Any]) -> List[Any]:
        ser = self.serialisation.serialise
        return [ser(i) for i in value]

    def deserialise(self, value: List[Any]) -> List[Any]:
        des = self.serialisation.deserialise
        return [des(v) for v in value]


class MapOf(Serialisation):
    def __init__(self, serialisation: Serialisation) -> None:
        self.serialisation = serialisation

    def serialise(self, value: Dict[Any, Any]) -> Dict[Any, Any]:
        ser = self.serialisation.serialise
        return {k: ser(v) for k, v in value.items()}

    def deserialise(self, value: Dict[Any, Any]) -> Dict[Any, Any]:
        des = self.serialisation.deserialise
        return {k: des(v) for k, v in value.items()}


V = TypeVar("V")


class Identity(Serialisation):
    def serialise(self, value: V) -> V:
        return value

    def deserialise(self, value: V) -> V:
        return value


class RFC3339Enc(Serialisation):
    def serialise(self, value: datetime.datetime) -> str:
        return _rfc3339.serialise(value)

    def deserialise(self, value: str) -> datetime.datetime:
        return _rfc3339.deserialise(value)


class ObjEnc(Serialisation):
    def __init__(self, cls: Type[JsonSchemaCompatible]) -> None:
        self._cls = cls

    def serialise(self, value: JsonSchemaCompatible) -> Dict[str, Any]:
        return value.to_json()

    def deserialise(self, value: Mapping[str, Any]) -> JsonSchemaCompatible:
        return self._cls.from_json(value)


class TimestampEnc(Serialisation):
    def serialise(self, value: datetime.datetime) -> int:
        return int(value.timestamp())

    def deserialise(self, value: int) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(value, datetime.timezone.utc)


E = TypeVar("E", bound=Enum)


class EnumEnc(Serialisation, Generic[E]):
    def __init__(self, cls: Type[E], by_name: bool = False) -> None:
        self._enum = cls
        self._byname = by_name

    def serialise(self, value: E) -> Any:
        return value.name if self._byname else value.value

    def deserialise(self, value: Any) -> E:
        return self._enum[value] if self._byname else self._enum(value)


RFC3339 = RFC3339Enc()
UNIX_TIMESTAMP = TimestampEnc()
