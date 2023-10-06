from dataclasses import dataclass
from typing import Any, Callable, Dict, Mapping, Optional

from .serialisation import Serialisation

NonEmptyPredicate = Callable[[Any], bool]


@(lambda cls: cls())
class MISSING:
    __slots__ = ()

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "<MISSING>"


@dataclass
class JSON:
    name: str
    omit_empty: bool = False
    nullable: bool = False
    serialisation: Optional[Serialisation] = None
    nonempty_predicate: Optional[NonEmptyPredicate] = None

    def _nonempty(self, value: Any) -> bool:
        nep = self.nonempty_predicate
        if nep is None:
            return value is not None
        return nep(value)

    def serialise(self, value: Any) -> Any:
        if value is None:
            return None

        return self.serialisation.serialise(value) if self.serialisation else value

    def deserialise(self, value: Any) -> Any:
        if value is None:
            return None
        return self.serialisation.deserialise(value) if self.serialisation else value

    def prepare(self, value: Any) -> Dict[str, Any]:
        """
        Perform the opposite operation of extract, with the value of the dataclass field.

        If the value is None or considered empty (via nonempty_predicate):
        - Return empty dict if `omit_empty` is True
        - Raise TypeError if `nullable` is False
        Otherwise return dict with name and value
        """

        if not self._nonempty(value):
            if self.omit_empty:
                return {}
            if not self.nullable:
                raise TypeError(f"Non-nullable field is empty: `{value}`")
        return {self.name: self.serialise(value)}

    def extract(self, data: Mapping[str, Any]) -> Any:
        """
        Attempt to extract and deserialise the key matching `self.name`

        If the key does not exist but the field is nullable, send back `MISSING` as a sentinel to not pass any
        value to the field for class instantiation.

        If the key exists, but the value is None, send it back as a value for nullable fields and raise error for
        non-nullable fields.

        Only non-None values are deserialised.
        """
        try:
            value = data[self.name]
        except LookupError:
            if self.omit_empty:
                return MISSING
            raise ValueError(f"Missing key '{self.name}' from input") from None
        else:
            if value is None:
                if not self.nullable:
                    raise ValueError(f"Value of '{self.name}' was `None` for non-nullable field")
                else:
                    return None
            return self.deserialise(value)
