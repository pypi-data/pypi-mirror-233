from enum import Enum
from typing import Any, List, Literal, Optional, Union

from pydantic import UUID4, Field, ValidationError, confloat, conint, conlist, field_validator

from ..commons import (
    ClassValue,
    DataCreatorType,
    Description,
    Id,
    ItemCount,
    Name,
    RestrictedBaseModel,
    Timestamp,
    Viewport,
)
from .classes import Class
from .commons import PostValidationBase

NppCreated = confloat(gt=0.0)
NppViewing = conlist(confloat(gt=0.0), min_length=2, max_length=2)
UniqueClassValue = Union[ClassValue, None]
Coordinate = conint(ge=0, strict=True)
Point = conlist(Coordinate, min_length=2, max_length=2)
Line = conlist(Point, min_length=2, max_length=2)
Polygon = conlist(Point, min_length=3)


class AnnotationType(str, Enum):
    POINT = "point"
    LINE = "line"
    ARROW = "arrow"
    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    POLYGON = "polygon"


class AnnotationReferenceType(str, Enum):
    WSI = "wsi"


# validator for jobs query
def validate_jobs(jobs):
    if jobs == [None]:
        raise ValueError("Queries with jobs: [null] are no longer supported")


# validator for class values query
def validate_class_values(class_values):
    if class_values is not None and None in class_values:
        raise ValueError("Queries with null in class value list are no longer supported")


# Post models
class PostAnnotationBase(PostValidationBase):
    id: Optional[UUID4] = Field(
        default=None,
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="ID of type UUID4 (only needed in post if external Ids enabled)",
    )
    name: Name = Field(examples=["Annotation Name"], description="Annotation name")
    description: Optional[Description] = Field(
        default=None, examples=["Annotation Description"], description="Annotation description"
    )
    creator_id: Id = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="Creator ID")
    creator_type: DataCreatorType = Field(examples=[DataCreatorType.SCOPE], description="Creator type")
    reference_id: Id = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of referenced Slide")
    reference_type: AnnotationReferenceType = Field(
        examples=[AnnotationReferenceType.WSI], description='Reference type (must be "wsi")'
    )
    npp_created: NppCreated = Field(
        examples=[499.0],
        description="Resolution in npp (nanometer per pixel) used to indicate on which layer the annotation is created",
    )
    npp_viewing: Optional[NppViewing] = Field(
        default=None,
        examples=[[499.0, 7984.0]],
        description="Recommended viewing resolution range in npp (nanometer per pixel) - Can be set by app",
    )
    centroid: Optional[Point] = Field(
        default=None,
        examples=[[100, 100]],
        description="Centroid of the annotation",
    )


class PostPointAnnotation(PostAnnotationBase):
    type: Literal["point"] = Field(examples=["point"], description="Point annotation")
    coordinates: Point = Field(examples=[[100, 200]], description="Point coordinates (must be >= 0)")


class PostLineAnnotation(PostAnnotationBase):
    type: Literal["line"] = Field(examples=["line"], description="Line annotation")
    coordinates: Line = Field(examples=[[[0, 100], [100, 100]]], description="Line coordinates (must be >= 0)")


class PostArrowAnnotation(PostAnnotationBase):
    type: Literal["arrow"] = Field(examples=["arrow"], description="Arrow annotation")
    head: Point = Field(examples=[[0, 100]], description="Point coordinates of arrow head (must be >= 0)")
    tail: Point = Field(examples=[[100, 150]], description="Point coordinates of arrow tail (must be >= 0)")


class PostCircleAnnotation(PostAnnotationBase):
    type: Literal["circle"] = Field(examples=["circle"], description="Circle annotation")
    center: Point = Field(examples=[[0, 100]], description="Point coordinates of center (must be >= 0)")
    radius: conint(gt=0, strict=True) = Field(examples=[100], description="Radius (must be > 0)")


class PostRectangleAnnotation(PostAnnotationBase):
    type: Literal["rectangle"] = Field(examples=["rectangle"], description="Rectangle annotation")
    upper_left: Point = Field(
        examples=[[0, 100]],
        description="Point coordinates of upper left corner of the rectangle (must be >= 0)",
    )
    width: conint(gt=0, strict=True) = Field(examples=[100], description="Rectangle width (must be > 0)")
    height: conint(gt=0, strict=True) = Field(examples=[200], description="Rectangle height (must be > 0)")


class PostPolygonAnnotation(PostAnnotationBase):
    type: Literal["polygon"] = Field(examples=["polygon"], description="Polygon annotation")
    coordinates: Polygon = Field(
        examples=[[[0, 100], [100, 100], [100, 0]]],
        description="Polygon coordinates (must be >= 0)",
    )


PostAnnotation = Union[
    PostPointAnnotation,
    PostLineAnnotation,
    PostArrowAnnotation,
    PostCircleAnnotation,
    PostRectangleAnnotation,
    PostPolygonAnnotation,
]


TYPE_MAPPING = {
    "point": PostPointAnnotation,
    "line": PostLineAnnotation,
    "arrow": PostArrowAnnotation,
    "circle": PostCircleAnnotation,
    "rectangle": PostRectangleAnnotation,
    "polygon": PostPolygonAnnotation,
}


def check_items(items, type_name):
    if len(items) > 0:
        if not TYPE_MAPPING[type_name].model_validate(items[0]):
            raise ValidationError()
    return items


class PostPointAnnotations(PostValidationBase):
    items: List[PostPointAnnotation] = Field(description="List of point annotations")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "point")


class PostLineAnnotations(PostValidationBase):
    items: List[PostLineAnnotation] = Field(description="List of line annotations")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "line")


class PostArrowAnnotations(PostValidationBase):
    items: List[PostArrowAnnotation] = Field(description="List of arrow annotations")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "arrow")


class PostCircleAnnotations(PostValidationBase):
    items: List[PostCircleAnnotation] = Field(description="List of circle annotations")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "circle")


class PostRectangleAnnotations(PostValidationBase):
    items: List[PostRectangleAnnotation] = Field(description="List of rectangle annotations")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "rectangle")


class PostPolygonAnnotations(PostValidationBase):
    items: List[PostPolygonAnnotation] = Field(description="List of polygon annotations")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "polygon")


PostAnnotationList = Union[
    PostPointAnnotations,
    PostLineAnnotations,
    PostArrowAnnotations,
    PostCircleAnnotations,
    PostRectangleAnnotations,
    PostPolygonAnnotations,
]

PostAnnotations = Union[PostAnnotationList, PostAnnotation]


# Full and post response models


class AnnotationBase(PostAnnotationBase):
    classes: Optional[List[Class]] = Field(
        default=None, description="List of classes assigned to annotation (if with_classes is true)"
    )
    created_at: Optional[Timestamp] = Field(
        default=None, examples=[1598611645], description="UNIX timestamp in seconds - set by server"
    )
    updated_at: Optional[Timestamp] = Field(
        default=None, examples=[1598611645], description="UNIX timestamp in seconds - set by server"
    )
    is_locked: Optional[bool] = Field(
        default=None,
        examples=["false"],
        description="Flag to mark an annotation as immutable",
    )


class PointAnnotation(AnnotationBase, PostPointAnnotation):
    pass


class LineAnnotation(AnnotationBase, PostLineAnnotation):
    pass


class ArrowAnnotation(AnnotationBase, PostArrowAnnotation):
    pass


class CircleAnnotation(AnnotationBase, PostCircleAnnotation):
    pass


class RectangleAnnotation(AnnotationBase, PostRectangleAnnotation):
    pass


class PolygonAnnotation(AnnotationBase, PostPolygonAnnotation):
    pass


Annotation = Union[
    PointAnnotation,
    LineAnnotation,
    ArrowAnnotation,
    CircleAnnotation,
    RectangleAnnotation,
    PolygonAnnotation,
]


class AnnotationCountResponse(RestrictedBaseModel):
    item_count: ItemCount = Field(examples=[12345], description="Count of all items")


class AnnotationListResponse(AnnotationCountResponse):
    items: List[Annotation] = Field(description="List of items")


class AnnotationIdList(RestrictedBaseModel):
    annotations: List[UUID4] = Field(
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of annotation ids (type UUID4)",
    )
    low_npp_centroids: Optional[List[conlist(conint(ge=0), min_length=2, max_length=2)]] = Field(
        default=None,
        examples=[[[100, 200], [2000, 5000], [987, 654]]],
        description=(
            "Centroids of all annotations with higher resolution (lower npp_created / npp_viewing values) "
            "than specified by npp_viewing in the query."
        ),
    )


Annotations = Union[Annotation, AnnotationListResponse]


class AnnotationList(AnnotationListResponse):
    low_npp_centroids: Optional[List[conlist(conint(ge=0), min_length=2, max_length=2)]] = Field(
        default=None,
        examples=[[[100, 200], [2000, 5000], [987, 654]]],
        description=(
            "Centroids of all annotations with higher resolution (lower npp_created / npp_viewing values) "
            "than specified by npp_viewing in the query."
        ),
    )


class UniqueClassValues(RestrictedBaseModel):
    unique_class_values: Optional[List[UniqueClassValue]] = Field(
        default=None,
        examples=[
            [
                "org.empaia.my_vendor.my_app.v1.classes.non_tumor",
                "org.empaia.my_vendor.my_app.v1.classes.tumor",
                None,
            ]
        ],
        description=(
            "List of unique class values for classes assigned to annotations matching given filter criteria. "
            "IMPORTANT NOTE: Can be null, if annotations without assigned classes are returned!"
        ),
    )


class AnnotationViewerList(RestrictedBaseModel):
    annotations: List[UUID4] = Field(
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of annotation Ids",
    )
    low_npp_centroids: List[conlist(conint(ge=0), min_length=2, max_length=2)] = Field(
        examples=[[[100, 200], [2000, 5000], [987, 654]]],
        description=(
            "Centroids of all annotations with higher resolution (lower npp_created / npp_viewing values) "
            "than specified by npp_viewing in the query."
        ),
    )


# Query models


class AnnotationUniqueClassesQuery(RestrictedBaseModel):
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
    references: Optional[conlist(Id, min_length=1)] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of reference Ids",
    )
    jobs: Optional[Union[conlist(Id, min_length=1), conlist(None, min_length=1, max_length=1)]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description=(
            "List of job Ids the annotations must be locked for. "
            "IMPORTANT NOTE: Can be a list with null as single value, "
            "if annotations not locked in any job should be returned!"
        ),
    )
    types: Optional[conlist(AnnotationType, min_length=1)] = Field(
        default=None,
        examples=[[AnnotationType.ARROW, AnnotationType.LINE]],
        description="List of annotation types",
    )
    viewport: Optional[Viewport] = Field(
        default=None,
        description="The viewport (only annotations within are returned)",
    )
    npp_viewing: Optional[NppViewing] = Field(
        default=None,
        examples=[[5.67, 7.89]],
        description="Resolution range in npp (nanometer per pixel) to filter annotations",
    )

    # jobs: [null] no longer supported ib v3 API; will be removed in v4 API
    @field_validator("jobs", mode="before")
    def pre_check_job_list(cls, jobs):
        validate_jobs(jobs)
        return jobs


class AnnotationViewerQuery(AnnotationUniqueClassesQuery):
    class_values: Optional[conlist(UniqueClassValue, min_length=1)] = Field(
        default=None,
        examples=[["org.empaia.my_vendor.my_app.v1.classes.non_tumor", "org.empaia.my_vendor.my_app.v1.classes.tumor"]],
        description=("List of class values."),
    )

    # jobs: [null] no longer supported ib v3 API; will be removed in v4 API
    @field_validator("class_values", mode="before")
    def pre_check_class_value_list(cls, class_values):
        validate_class_values(class_values)
        return class_values


class AnnotationQuery(AnnotationViewerQuery):
    annotations: Optional[conlist(Any, min_length=1)] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of Annotation Ids (must be of type UUID4)",
    )


class AnnotationQueryPosition(RestrictedBaseModel):
    id: UUID4 = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of type UUID4")
    position: conint(ge=0) = Field(
        examples=[42], description="Position of annotation in result of query (starts with 0)"
    )
