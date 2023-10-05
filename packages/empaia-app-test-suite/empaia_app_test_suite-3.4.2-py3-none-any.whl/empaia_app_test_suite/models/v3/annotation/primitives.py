from enum import Enum
from typing import Any, List, Literal, Optional, Union

from pydantic import UUID4, Field, StrictInt, ValidationError, conlist, constr, field_validator, model_validator

from ..commons import DataCreatorType, Description, Id, ItemCount, Name, RestrictedBaseModel, validate_reference
from .commons import PostValidationBase

StringPrimitiveValue = constr(strip_whitespace=True, min_length=1, max_length=200)


class PrimitiveType(str, Enum):
    INTEGER = "integer"
    FLOAT = "float"
    BOOL = "bool"
    STRING = "string"


class PrimitiveReferenceType(str, Enum):
    ANNOTATION = "annotation"
    COLLECTION = "collection"
    WSI = "wsi"


# Post models


class PostPrimitveBase(PostValidationBase):
    id: Optional[UUID4] = Field(
        default=None,
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="ID of type UUID4 (only needed in post if external Ids enabled)",
    )
    name: Name = Field(examples=["Primitive Name"], description="Primitive name")
    description: Optional[Description] = Field(
        default=None, examples=["Primitive Description"], description="Primitive description"
    )
    creator_id: Id = Field(
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="Id of the creator of this primitive",
    )
    creator_type: DataCreatorType = Field(examples=[DataCreatorType.JOB], description="Creator type")
    reference_id: Optional[Id] = Field(
        default=None,
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="Id of the object referenced by this primitive",
    )
    reference_type: Optional[PrimitiveReferenceType] = Field(
        default=None, examples=[PrimitiveReferenceType.COLLECTION], description="Reference type"
    )

    # validator for reference
    @model_validator(mode="before")
    def check_reference(cls, data):
        reference_type = "reference_type" in data
        reference_id = "reference_id" in data
        validate_reference(reference_id=reference_id, reference_type=reference_type)
        return data


class PostIntegerPrimitive(PostPrimitveBase):
    type: Literal["integer"] = Field(examples=["integer"], description="Integer type")
    value: StrictInt = Field(examples=[42], description="Integer value")


class PostFloatPrimitive(PostPrimitveBase):
    type: Literal["float"] = Field(examples=["float"], description="Float type")
    value: float = Field(examples=[0.42], description="Float value")


class PostBoolPrimitive(PostPrimitveBase):
    type: Literal["bool"] = Field(examples=["bool"], description="Bool type")
    value: bool = Field(examples=["True"], description="Bool value")


class PostStringPrimitive(PostPrimitveBase):
    type: Literal["string"] = Field(examples=["string"], description="String type")
    value: StringPrimitiveValue = Field(examples=["Positive"], description="String value")


PostPrimitive = Union[PostIntegerPrimitive, PostFloatPrimitive, PostBoolPrimitive, PostStringPrimitive]


TYPE_MAPPING = {
    "integer": PostIntegerPrimitive,
    "float": PostFloatPrimitive,
    "bool": PostBoolPrimitive,
    "string": PostStringPrimitive,
}


def check_items(items, type_name):
    if len(items) > 0:
        if not TYPE_MAPPING[type_name].model_validate(items[0]):
            raise ValidationError()
    return items


class PostIntegerPrimitives(PostValidationBase):
    items: List[PostIntegerPrimitive] = Field(description="List of integer primitives")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "integer")


class PostFloatPrimitives(PostValidationBase):
    items: List[PostFloatPrimitive] = Field(description="List of float primitives")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "float")


class PostBoolPrimitives(PostValidationBase):
    items: List[PostBoolPrimitive] = Field(description="List of bool primitives")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "bool")


class PostStringPrimitives(PostValidationBase):
    items: List[PostStringPrimitive] = Field(description="List of string primitives")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "string")


PostPrimitiveList = Union[PostIntegerPrimitives, PostFloatPrimitives, PostBoolPrimitives, PostStringPrimitives]


PostPrimitives = Union[PostPrimitiveList, PostPrimitive]


# Full and post response models


class PrimitiveBase(PostPrimitveBase):
    is_locked: Optional[bool] = Field(
        default=None,
        examples=["false"],
        description="Flag to mark a primitive as immutable",
    )


class IntegerPrimitive(PrimitiveBase, PostIntegerPrimitive):
    pass


class FloatPrimitive(PrimitiveBase, PostFloatPrimitive):
    pass


class BoolPrimitive(PrimitiveBase, PostBoolPrimitive):
    pass


class StringPrimitive(PrimitiveBase, PostStringPrimitive):
    pass


Primitive = Union[IntegerPrimitive, FloatPrimitive, BoolPrimitive, StringPrimitive]


class PrimitiveList(RestrictedBaseModel):
    item_count: ItemCount = Field(examples=[12345], description="Count of all items")
    items: List[Primitive] = Field(description="List of items")


Primitives = Union[Primitive, PrimitiveList]


# Query model


class PrimitiveQuery(RestrictedBaseModel):
    creators: Optional[conlist(Id, min_length=1)] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of creator Ids",
    )
    references: Optional[conlist(Union[Id, None], min_length=1)] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                None,
            ]
        ],
        description=(
            "List of reference Ids. IMPORTANT NOTE: Can be null, if primitives without reference should be included!"
        ),
    )
    jobs: Optional[conlist(Id, min_length=1)] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of job Ids",
    )
    types: Optional[conlist(PrimitiveType, min_length=1)] = Field(
        default=None,
        examples=[[PrimitiveType.INTEGER, PrimitiveType.FLOAT]],
        description="List of primitive types",
    )
    primitives: Optional[conlist(Any, min_length=1)] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of Primitive Ids (must be of type UUID4)",
    )
