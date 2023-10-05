from enum import Enum
from typing import Any, List, Literal, Optional, Union

from pydantic import UUID4, Field, ValidationError, conlist, field_validator

from ..commons import ClassValue, DataCreatorType, Id, ItemCount, RestrictedBaseModel
from .commons import PostValidationBase


class ClassReferenceType(str, Enum):
    ANNOTATION = "annotation"


# Post models


class PostClass(PostValidationBase):
    id: Optional[UUID4] = Field(
        default=None,
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="ID of type UUID4 (only needed in post if external Ids enabled)",
    )
    type: Literal["class"] = Field(examples=["class"], description='Item of type "class"')
    creator_id: Id = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="Creator ID")
    creator_type: DataCreatorType = Field(examples=[DataCreatorType.JOB], description="Creator type")
    value: ClassValue = Field(
        examples=["org.empaia.my_vendor.my_app.v1.classes.non_tumor"],
        description="Either a value from EMPAIA App Description or a permitted global class value",
    )
    reference_id: UUID4 = Field(
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="ID of type UUID4 - ID of referenced annotation",
    )
    reference_type: ClassReferenceType = Field(
        examples=[ClassReferenceType.ANNOTATION], description='Reference type (must be "annotation")'
    )


class PostClassList(PostValidationBase):
    items: List[PostClass] = Field(description="List of classes")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        if len(v) > 0:
            if not PostClass.model_validate(v[0]):
                raise ValidationError()
        return v


PostClasses = Union[PostClassList, PostClass]


# Full and post response models


class Class(PostClass):
    is_locked: Optional[bool] = Field(default=None, examples=["false"], description="Flag to mark a class as immutable")


class ClassListResponse(RestrictedBaseModel):
    item_count: ItemCount = Field(examples=[12345], description="Count of all items ")
    items: List[Class] = Field(description="List of items")


Classes = Union[Class, ClassListResponse]


class ClassList(ClassListResponse):
    unique_class_values: Optional[List[ClassValue]] = Field(
        default=None,
        examples=[
            [
                "org.empaia.my_vendor.my_app.v1.classes.non_tumor",
                "org.empaia.my_vendor.my_app.v1.classes.tumor",
            ]
        ],
        description="List of unique class values (for classes matching given filter criteria when returned by query)",
    )


# Query model


class ClassQuery(RestrictedBaseModel):
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
    references: Optional[conlist(UUID4, min_length=1)] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of annotation Ids (UUID type 4)",
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
    classes: Optional[conlist(Any, min_length=1)] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of Class Ids (must be of type UUID4)",
    )
