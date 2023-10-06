from dataclasses import MISSING as DC_MISSING
from dataclasses import Field, InitVar, dataclass, is_dataclass
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from typing_extensions import dataclass_transform

from jsonnotate.serialisation import JsonSchemaCompatible, ObjEnc

from .attributes import JSON, MISSING

C = TypeVar("C", bound="JsonSchema")

if TYPE_CHECKING:
    FieldType = Field[Any]
else:
    FieldType = Field


def is_missing(value: Any) -> bool:
    """The dataclass machinery sets a sentinel value for fields with no default value"""
    return value is DC_MISSING


def has_default(value: FieldType) -> bool:
    return not is_missing(value.default) or not is_missing(value.default_factory)


def get_json_attribute(typ: Any) -> Optional[JSON]:
    """Extract annotated JSON metadata, if any"""
    origin = get_origin(typ)
    if origin is Annotated:
        for param in get_args(typ)[1:]:
            if isinstance(param, JSON):
                return param
    elif origin is ClassVar:
        return get_json_attribute(get_args(typ)[0])
    return None


def is_optional(typ: Any) -> bool:
    """Check if field is marked as Optional. Optional is represented as Union[type, None]."""
    origin = get_origin(typ)
    if origin is Union:
        return type(None) in get_args(typ)
    if origin is Annotated:
        return is_optional(get_args(typ)[0])
    return False


def get_json_compat(typ: type) -> Optional[type]:
    """
    Helper method to determine if the underlying type qualifies as JsonSchemaCompatible

    Useful for detecting and implementing automatic jsonnotate.serialisation.ObjEnc for fields.
    """
    origin = get_origin(typ)
    if origin is Annotated:
        return get_json_compat(get_args(typ)[0])
    elif origin is not None:
        # Filter out NoneType, as that just signals Optional which is fine
        potential_types = [arg for arg in get_args(typ) if arg is not type(None)]
        if len(potential_types) == 1:
            return get_json_compat(potential_types[0])
        else:
            return None
    if issubclass(typ, JsonSchemaCompatible):
        return typ
    return None


def create_builder(found_fields: List[Tuple[FieldType, JSON]]) -> Callable[[Type[C], Dict[str, Any]], C]:
    def from_json(cls: Type[C], data: Mapping[str, Any]) -> C:
        kwargs: Dict[str, Any] = {
            f.name: v for f, v in ((f, j.extract(data)) for f, j in found_fields) if v is not MISSING
        }
        return cls(**kwargs)

    return from_json


def create_writer(found_fields: List[Tuple[FieldType, JSON]]) -> Callable[[C], Dict[str, Any]]:
    def to_json(self: C) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        for f, j in found_fields:
            data.update(j.prepare(getattr(self, f.name)))
        return data

    return to_json


def collect(cls: type, *, annotated_only: bool, auto_serialise: bool) -> List[Tuple[FieldType, JSON]]:
    """
    Iterate all dataclass fields on the given type, extracting (or creating) JSON annotations for each field.

    The final list of fields must allow for valid instantiation of the dataclass.
    """
    if not is_dataclass(cls):
        raise TypeError("Class must be a dataclass")

    cls_builders: List[Tuple[FieldType, JSON]] = []

    for field in cls.__dataclass_fields__.values():
        json = validate_field(field, annotated_only=annotated_only, auto_serialise=auto_serialise)
        if json is not None:
            cls_builders.append((field, json))

    return cls_builders


def validate_field(field: FieldType, annotated_only: bool, auto_serialise: bool) -> Optional[JSON]:
    typ = field.type
    origin = get_origin(typ)
    json = get_json_attribute(typ)

    if origin is ClassVar:
        if json is not None:
            raise TypeError("JSON attributes found on class variable.")
        return None
    if not field.init:
        return None
    if origin is InitVar:
        # init-only, if this has no defaults we can't create from json
        if not has_default(field):
            raise TypeError(
                f"Init-only field {field.name} has no default, cannot generate from_json() method. "
                "If this is optional, please set a default."
            )
        # TODO: support initvars from json
        return None
    if json is None:
        if not annotated_only:
            json = JSON(field.name, nullable=is_optional(typ))
        else:
            if not has_default(field):
                raise TypeError(
                    f"Field {field.name} has no default, cannot generate from_json() method. "
                    "If this is optional, please set a default."
                )
            return None
    if json.nullable and not is_optional(typ):
        raise TypeError(f"Field {field.name} is nullable but type is not Optional[...]")
    if json.omit_empty and not has_default(field):
        raise TypeError(f"Field {field.name} is omit_empty but has no default")

    if json.serialisation is None and auto_serialise:
        compat_type = get_json_compat(typ)
        if compat_type:
            json.serialisation = ObjEnc(compat_type)

    return json


@dataclass_transform()
class JsonSchema:
    if TYPE_CHECKING:

        @classmethod
        def _inner_from_json(cls: Type[C], data: Mapping[str, Any]) -> C:
            ...

        def _inner_to_json(self: C) -> Dict[str, Any]:
            ...

    @classmethod
    def from_json(cls: Type[C], data: Mapping[str, Any]) -> C:
        return cls._inner_from_json(data)

    def to_json(self: C) -> Dict[str, Any]:
        return self._inner_to_json()

    def __init_subclass__(
        cls: Type[C], annotated_only: bool = True, auto_serialise: bool = False, **kwds: Any
    ) -> None:
        """
        Turn the subclass into a dataclass, and add to/from_json methods.

        - `annotated_only`: If set to True, only fields that are annotated with a JSON attribute will be included in
          the `to/from_json` methods. If false, all fields will be included.
        - `auto_serialise`: If set to True, any fields with a type that is JsonSchemaCompatible will use the ObjeEnc
          serialisation (unless one is already explicitly set).

        Note that setting `annotated_only=False` is not guaranteed to work for all fields, and may throw runtime
        errors.

        Any other keyword arguments are passed to the dataclass decorator (frozen, order, eq, etc.).
        """
        datacls = dataclass(cls, **kwds)
        found_fields = collect(datacls, annotated_only=annotated_only, auto_serialise=auto_serialise)

        setattr(datacls, "_inner_from_json", classmethod(create_builder(found_fields)))
        setattr(datacls, "_inner_to_json", create_writer(found_fields))
