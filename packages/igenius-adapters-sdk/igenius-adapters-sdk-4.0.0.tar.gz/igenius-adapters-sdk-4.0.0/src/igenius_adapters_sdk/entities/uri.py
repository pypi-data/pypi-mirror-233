import re
from os import environ
from typing import Any, Optional, Pattern

from pydantic import BaseModel, errors


__all__ = [
    "AttributeUid",
    "AttributeUri",
    "CollectionUid",
    "CollectionUri",
    "DatasourceUid",
    "DatasourceUri",
    "Uid",
]

OptionalInt = Optional[int]
RE_MATCH_COLLECTION_NAME = re.compile(r"" + environ.get("IGENIUS_ADAPTER_SDK_RE_MATCH_COLLECTION_NAME", r"^\S+$"))
RE_MATCH_ALL_BUT_NEW_LINES_AND_TABS = re.compile(
    r"" + environ.get("IGENIUS_ADAPTER_SDK_RE_MATCH_ATTRIBUTE_NAME", r"^[\S ]+$")
)


class StrUid(type):
    def __instancecheck__(self, instance):
        return instance.__class__.__name__ == "str"


class Uid(metaclass=StrUid):
    min_length: int = 1
    max_length: OptionalInt = None
    regex: Optional[Pattern[str]] = RE_MATCH_ALL_BUT_NEW_LINES_AND_TABS

    val: str = None

    def __init__(self, val) -> None:
        self.__set__(None, val)

    @classmethod
    def validate_format(cls, value):
        if not isinstance(value, str):
            raise errors.PydanticUserError(code="", message=f"Expected str as valid uid not {value.__class__.__name__}")
        if len(value) < cls.min_length:
            raise errors.PydanticUserError(code="", message=f"length of value < {cls.min_length}")
        if cls.max_length and len(value) > cls.max_length:
            raise errors.PydanticUserError(code="", message=f"length of value > {cls.max_length}")
        if cls.regex:
            if not cls.regex.match(value):
                raise errors.PydanticUserError(
                    code="", message=f"Invalid uid value. Should validate this regex {cls.regex}"
                )
        return value

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self.val)

    def __get__(self):
        return self.val

    def __set__(self, _, val):
        self.validate_format(val)
        self.val = val

    def __call__(self) -> str:
        return self.__str__()

    def __eq__(self, __value: object) -> bool:
        return self.val == __value

    def __ne__(self, __value: object) -> bool:
        return self.val != __value

    def __le__(self, __value: object) -> bool:
        return self.val <= __value

    def __ge__(self, __value: object) -> bool:
        return self.val >= __value

    def __lt__(self, other):
        return self.val < other

    def __gt__(self, other):
        return self.val > other

    def __len__(self):
        return len(self.val)

    def __hash__(self) -> int:
        return hash(self.val)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.val, name)

    # contains support
    def __contains__(self, c: str) -> bool:
        return c in self.val

    def __getitem__(self, index):
        return self.val[index]


class AttributeUid(Uid):
    pass


class CollectionUid(Uid):
    regex: Pattern[str] = RE_MATCH_COLLECTION_NAME


class DatasourceUid(Uid):
    pass


class UriModel(BaseModel):
    def __hash__(self):
        return hash(tuple(self.model_dump().items()))

    class Config:
        frozen = True


class DatasourceUri(UriModel):
    datasource_uid: DatasourceUid

    class Config:
        arbitrary_types_allowed = True


class CollectionUri(UriModel):
    datasource_uid: DatasourceUid
    collection_uid: CollectionUid

    class Config:
        arbitrary_types_allowed = True


class AttributeUri(UriModel):
    datasource_uid: DatasourceUid
    collection_uid: CollectionUid
    attribute_uid: AttributeUid

    class Config:
        arbitrary_types_allowed = True
