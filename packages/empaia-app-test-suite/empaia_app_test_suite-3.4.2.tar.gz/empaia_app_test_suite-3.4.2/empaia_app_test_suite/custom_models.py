from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict

from empaia_app_test_suite.models.v3.annotation.annotations import (
    PostArrowAnnotation,
    PostCircleAnnotation,
    PostLineAnnotation,
    PostPointAnnotation,
    PostPolygonAnnotation,
    PostRectangleAnnotation,
)
from empaia_app_test_suite.models.v3.annotation.classes import PostClass
from empaia_app_test_suite.models.v3.annotation.primitives import (
    PostBoolPrimitive,
    PostFloatPrimitive,
    PostIntegerPrimitive,
    PostStringPrimitive,
)

for _class in (
    PostPointAnnotation,
    PostLineAnnotation,
    PostArrowAnnotation,
    PostCircleAnnotation,
    PostRectangleAnnotation,
    PostPolygonAnnotation,
    PostIntegerPrimitive,
    PostFloatPrimitive,
    PostBoolPrimitive,
    PostStringPrimitive,
    PostClass,
):
    del _class.model_fields["creator_type"]
    del _class.model_fields["creator_id"]


class ApiDataType(Enum):
    ANNOTATIONS = "annotations"
    PRIMITIVES = "primitives"
    CLASSES = "classes"
    COLLECTIONS = "collections"
    SLIDES = "slides"


class InputParameter(BaseModel):
    input_key: str  # key in ead.inputs
    post_data: dict
    api_data_type: ApiDataType
    reference_ids: List[str]  # multiple if collection


class WsiInput(BaseModel):
    type: Literal["wsi"]
    id: Optional[str] = None
    path: str
    tissue: str = "KIDNEY"
    stain: str = "H_AND_E"
    block: str = "block123"

    model_config = ConfigDict(extra="forbid")


class OptionalForTestSuitePrimitive(BaseModel):
    name: Optional[str] = None
    creator_type: Optional[str] = None
    creator_id: Optional[str] = None


class OptionalForTestSuite(OptionalForTestSuitePrimitive):
    reference_type: Optional[str] = None


class ClassInput(PostClass, OptionalForTestSuite):
    pass


class IntegerInput(PostIntegerPrimitive, OptionalForTestSuitePrimitive):
    pass


class FloatInput(PostFloatPrimitive, OptionalForTestSuitePrimitive):
    pass


class BoolInput(PostBoolPrimitive, OptionalForTestSuitePrimitive):
    pass


class StringInput(PostStringPrimitive, OptionalForTestSuitePrimitive):
    pass


class PointInput(PostPointAnnotation, OptionalForTestSuite):
    pass


class LineInput(PostLineAnnotation, OptionalForTestSuite):
    pass


class ArrowInput(PostArrowAnnotation, OptionalForTestSuite):
    pass


class CircleInput(PostCircleAnnotation, OptionalForTestSuite):
    pass


class RectangleInput(PostRectangleAnnotation, OptionalForTestSuite):
    pass


class PolygonInput(PostPolygonAnnotation, OptionalForTestSuite):
    pass


class CollectionInput(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    reference_type: Optional[str] = None
    creator_id: Optional[str] = None
    creator_type: Optional[str] = None
    is_locked: Optional[bool] = None
    item_type: Literal[
        "integer",
        "float",
        "bool",
        "string",
        "point",
        "line",
        "arrow",
        "circle",
        "rectangle",
        "polygon",
        "wsi",
        "class",
        "collection",
    ]
    item_count: Optional[int] = None
    items: Union[
        List[IntegerInput],
        List[FloatInput],
        List[BoolInput],
        List[StringInput],
        List[PointInput],
        List[LineInput],
        List[ArrowInput],
        List[CircleInput],
        List[RectangleInput],
        List[PolygonInput],
        List[WsiInput],
        List[ClassInput],
        List["CollectionInput"],
    ]


CollectionInput.model_rebuild()


TYPE_MODEL_MAP = {
    "integer": IntegerInput,
    "float": FloatInput,
    "bool": BoolInput,
    "string": StringInput,
    "point": PointInput,
    "line": LineInput,
    "arrow": ArrowInput,
    "circle": CircleInput,
    "rectangle": RectangleInput,
    "polygon": PolygonInput,
    "wsi": WsiInput,
    "class": ClassInput,
    "collection": CollectionInput,
}
