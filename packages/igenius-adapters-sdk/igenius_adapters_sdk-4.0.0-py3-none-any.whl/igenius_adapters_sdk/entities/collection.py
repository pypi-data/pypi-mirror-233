from enum import Enum
from typing import List, Literal, Mapping, NewType, Union, Any

from pydantic import BaseModel, Field, model_validator


class AttributeType(str, Enum):
    BOOLEAN = "crystal.topics.data.attribute-types.boolean"
    CATEGORICAL = "crystal.topics.data.attribute-types.categorical"
    DATETIME = "crystal.topics.data.attribute-types.datetime"
    NUMERIC = "crystal.topics.data.attribute-types.numeric"
    RELATIVE_TIME_RANGE = "crystal.topics.data.attribute-types.relative_timerange"
    STRUCT = "crystal.topics.data.attribute-types.scruct"
    ARRAY = "crystal.topics.data.attribute-types.array"
    UNKNOWN = "crystal.topics.data.attribute-types.unknown"


AttributeUid = NewType("AttributeUid", str)


class Attribute(BaseModel):
    uid: AttributeUid
    type: AttributeType  # noqa: A003
    filterable: bool
    sortable: bool

    @model_validator(mode="before")
    @classmethod
    def always_uid_str(cls, data: Any) -> str:
        if isinstance(data, dict):
            if data.get("uid", None):
                data["uid"] = str(data["uid"])
        return data


class AttributesSchema(BaseModel):
    attributes: List[Attribute] = Field(default=list())


CollectionUid = NewType("CollectionUid", str)


class Collection(BaseModel):
    uid: CollectionUid
    attributes_schema: AttributesSchema


AttributeFilter = Union[Literal["*"], List[AttributeUid]]


CollectionFilter = Mapping[CollectionUid, AttributeFilter]
