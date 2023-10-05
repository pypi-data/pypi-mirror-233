import json
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import (
    UUID4,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    conint,
    conlist,
    constr,
    model_validator,
)

from ..commons import RestrictedBaseModel

ItemCount = conint(ge=0)
Timestamp = conint(ge=0)

VersionConstraint = constr(pattern=r"^(\d+\.)?(\d+\.)?(\d+\.)(\*|\d+)$")

ConfigurationModel = Dict[StrictStr, Union[StrictStr, StrictInt, StrictFloat, StrictBool]]


config_section_example = {
    "some_token": "secret-token",
    "some_flag": True,
    "some_parameter": 42,
    "some_other_param": 42.5,
}


class AppMediaPurpose(str, Enum):
    PEEK = "peek"
    BANNER = "banner"
    WORKFLOW = "workflow"
    MANUAL = "manual"


class ListingStatus(str, Enum):
    LISTED = "LISTED"
    DELISTED = "DELISTED"
    ADMIN_DELISTED = "ADMIN_DELISTED"
    DRAFT = "DRAFT"


class AppStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    DRAFT = "DRAFT"


class ApiVersion(str, Enum):
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"


class Language(str, Enum):
    DE = "DE"
    EN = "EN"


class AppConfigurationType(str, Enum):
    GLOBAL = "global"
    CUSTOMER = "customer"


class Browser(str, Enum):
    FIREFOX = "firefox"
    CHROME = "chrome"
    EDGE = "edge"
    SAFARI = "safari"


class OS(str, Enum):
    Win10 = "win10"
    Win11 = "win11"
    Linux = "linux"
    MacOS = "macOS"


class TextTranslation(RestrictedBaseModel):
    lang: Language = Field(examples=[Language.EN], description="Language abbreviation")
    text: str = Field(examples=["Some text"], description="Translated tag name")


class PostAppTag(RestrictedBaseModel):
    tag_group: str = Field(examples=["TISSUE"], description="Tag group. See definitions for valid tag groups.")
    tag_name: str = Field(examples=["SKIN"], description="Tag name. See definitions for valid tag names.")


class AppTag(RestrictedBaseModel):
    name: str = Field(examples=["SKIN"], description="Tag name. See definitions for valid tag names.")
    tag_translations: List[TextTranslation]


class TagList(RestrictedBaseModel):
    tissues: List[AppTag] = Field(default=[], description="List of tissues")
    stains: List[AppTag] = Field(default=[], description="List of stains")
    indications: List[AppTag] = Field(default=[], description="List of indications")
    analysis: List[AppTag] = Field(default=[], description="List of analysis")
    clearances: List[AppTag] = Field(default=[], description="List of market clearances / certifications")


class MediaMetadata(RestrictedBaseModel):
    caption: Optional[Dict[str, str]] = Field(
        default=None,
        examples=[{"EN": "Description in english", "DE": "Beschreibung auf Deutsch"}],
        description="Caption",
    )
    alternative_text: Optional[Dict[str, str]] = Field(
        default=None,
        examples=[{"EN": "Description in english", "DE": "Beschreibung auf Deutsch"}],
        description="Alternative text",
    )

    @model_validator(mode="before")
    def validate_model(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))  # pylint: disable=E1102
        return value


class ResizedMediaUrlsObject(RestrictedBaseModel):
    w60: Optional[str] = Field(
        default=None,
        examples=["https://url.to/image_w60"],
        description="Presigned url to the media object with max width 60px",
    )
    w400: Optional[str] = Field(
        default=None,
        examples=["https://url.to/image_w400"],
        description="Presigned url to the media object with max width 400px",
    )
    w800: Optional[str] = Field(
        default=None,
        examples=["https://url.to/image_w800"],
        description="Presigned url to the media object with max width 800x",
    )
    w1200: Optional[str] = Field(
        default=None,
        examples=["https://url.to/image_w1200"],
        description="Presigned url to the media object with max width 1200px",
    )


class MediaObjectCore(RestrictedBaseModel):
    index: int = Field(
        examples=[2], description="Number of the step, required when media purpose is 'PREVIEW', 'BANNER' or 'WORKFLOW"
    )
    caption: Optional[List[TextTranslation]] = Field(default=None, description="Media caption")
    alt_text: Optional[List[TextTranslation]] = Field(
        default=None,
        description="Alternative text for media",
    )
    internal_path: str = Field(examples=["/internal/path/to"], description="Internam Minio path")
    content_type: str = Field(examples=["image/jpeg"], description="Content type of the media object")
    presigned_media_url: Optional[str] = Field(
        default=None, examples=["https://url.to/image"], description="Presigned url to the media object"
    )
    resized_presigned_media_urls: Optional[ResizedMediaUrlsObject] = Field(
        default=None, description="Resized versions of an image media object"
    )


class MediaObject(MediaObjectCore):
    id: UUID4 = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="Media ID")


PostMediaObject = MediaObjectCore


class MediaList(RestrictedBaseModel):
    peek: List[MediaObject] = Field(default=[], description="Peek media")
    banner: List[MediaObject] = Field(default=[], description="Banner media")
    workflow: List[MediaObject] = Field(default=[], description="Workflow media")
    manual: List[MediaObject] = Field(default=[], description="Manual media")


# App UI Config


# CSP - unsafe-inline and unsafe-eval policy settings for supported *-src csp directives
class AppUiConfigSrcPolicies(RestrictedBaseModel):
    unsafe_inline: Optional[bool] = Field(
        default=None, examples=[True], description="Set unsafe-inline for App-UI code if set to 'true'."
    )
    unsafe_eval: Optional[bool] = Field(
        default=None, examples=[True], description="Set unsafe-eval for App-UI code if set to 'true'."
    )


class AppUiCspConfiguration(RestrictedBaseModel):
    script_src: Optional[AppUiConfigSrcPolicies] = Field(
        default=None, description="CSP script-src setting for App-UIs."
    )
    style_src: Optional[AppUiConfigSrcPolicies] = Field(default=None, description="CSP style-src setting for App-UIs.")
    font_src: Optional[AppUiConfigSrcPolicies] = Field(default=None, description="CSP font-src setting for App-UIs.")


class AppUiIframeConfiguration(RestrictedBaseModel):
    allow_popups: Optional[bool] = Field(
        default=None,
        examples=[True],
        description="Set to 'true' if an App UI is allowed to redirect in external popup.",
    )


class AppUiTested(RestrictedBaseModel):
    browser: Browser = Field(examples=[Browser.CHROME], description="App UI tested for browser")
    version: VersionConstraint = Field(examples=["102.32.552"], description="App UI tested for browser version")
    os: OS = Field(examples=[OS.Win11], description="App UI tested on operating system")


class AppUiConfiguration(RestrictedBaseModel):
    csp: Optional[AppUiCspConfiguration] = Field(default=None, description="CSP settings for App-UIs.")
    iframe: Optional[AppUiIframeConfiguration] = Field(default=None, description="Iframe settings for App-UIs.")
    tested: Optional[List[AppUiTested]] = Field(
        default=None, description="Tested combination of browser and OS for an App UI."
    )
    model_config = ConfigDict(from_attributes=True)


# App


class AppDetailsCore(RestrictedBaseModel):
    name: str = Field(examples=["PD-L1 Quantifier"], description="Qualified app name displayed in the portal")


class PostAppDetails(AppDetailsCore):
    description: Dict[str, str] = Field(
        examples=[{"EN": "Description in english", "DE": "Beschreibung auf Deutsch"}], description="Description"
    )


class AppDetails(AppDetailsCore):
    marketplace_url: str = Field(examples=["http://url.to/store"], description="Url to app in the marketplace")
    description: List[TextTranslation] = Field(description="Description")


class PostApp(RestrictedBaseModel):
    ead: Optional[dict] = Field(default=None, examples=[{}], description="EAD content of the app")
    registry_image_url: Optional[str] = Field(
        default=None,
        examples=["https://registry.gitlab.com/empaia/integration/ap_xyz"],
        description="Url to the container image in the registry",
    )
    app_ui_url: Optional[str] = Field(
        default=None, examples=["http://app1.emapaia.org"], description="Url where the app UI is located"
    )
    app_ui_configuration: Optional[AppUiConfiguration] = Field(
        default=None, examples=[{}], description="App UI configuration"
    )


class PostAdminApp(PostApp):
    id: Optional[UUID4] = Field(
        default=None, examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="External ID of the app"
    )


class PostActiveAdminApps(RestrictedBaseModel):
    v1: Optional[PostAdminApp] = Field(default=None, description="App for EAD v1-darft3 without App UI (WBC 1.0)")
    v2: Optional[PostAdminApp] = Field(default=None, description="App for EAD v1-darft3 with App UI (WBC 2.0)")
    v3: Optional[PostAdminApp] = Field(default=None, description="App for EAD v3")


class PublicApp(PostApp):
    id: UUID4 = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of the app")
    version: Optional[str] = Field(default=None, examples=["v1.2"], description="Version of the app")
    has_frontend: bool = Field(examples=[True], description="If true, app is shipped with a frontend")


class ClosedApp(PublicApp):
    status: AppStatus = Field(examples=[AppStatus.DRAFT], description="Status of the app")
    portal_app_id: UUID4 = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of the portal app")
    creator_id: str = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="Creator ID")
    created_at: Timestamp = Field(examples=[1598611645], description="UNIX timestamp in seconds - set by server")
    updated_at: Timestamp = Field(examples=[1598611645], description="UNIX timestamp in seconds - set by server")


# Portal App View


class AppViewCore(RestrictedBaseModel):
    non_functional: Optional[bool] = Field(
        examples=[False],
        default=False,
        description="If true, portal app can be listed although technical app is not yet available",
    )
    research_only: bool = Field(
        examples=[False],
        default=False,
        description="If true, app is intended to be used for reasearch only",
    )


class PostAdminAppView(AppViewCore):
    details: Optional[PostAppDetails] = None
    tags: Optional[List[PostAppTag]] = None
    app: PostAdminApp


class PublicAppView(AppViewCore):
    version: Optional[str] = Field(default=None, examples=["v1.2"], description="Version of the currently active app")
    details: Optional[AppDetails] = None
    media: Optional[MediaList] = None
    tags: Optional[TagList] = None
    created_at: Timestamp = Field(examples=[1598611645], description="UNIX timestamp in seconds - set by server")
    reviewed_at: Optional[Timestamp] = Field(
        default=None, examples=[1598611645], description="UNIX timestamp in seconds - set by server"
    )


class PublicActiveAppViews(RestrictedBaseModel):
    v1: Optional[PublicAppView] = Field(default=None, description="App view for EAD v1-darft3 without App UI (WBC 1.0)")
    v2: Optional[PublicAppView] = Field(default=None, description="App view for EAD v1-darft3 with App UI (WBC 2.0)")
    v3: Optional[PublicAppView] = Field(default=None, description="App view for EAD v3")


class ClosedAppView(PublicAppView):
    id: UUID4 = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of the app view")
    portal_app_id: UUID4 = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of the portal app")
    organization_id: str = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="Organization ID")
    status: AppStatus = Field(examples=[AppStatus.DRAFT], descritpion="Status of the app")
    app: Optional[ClosedApp] = None
    creator_id: str = Field(
        default=None, examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of the app view creator"
    )
    review_comment: Optional[str] = Field(
        default=None, examples=["Review comment"], description="Review commet, i.e. in case of rejection"
    )
    api_version: ApiVersion = Field(examples=[ApiVersion.V1], description="Supported API version by this app view")
    reviewer_id: Optional[str] = Field(
        default=None, examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of the reviewer"
    )


class ClosedActiveAppViews(RestrictedBaseModel):
    v1: Optional[ClosedAppView] = Field(default=None, description="App view for EAD v1-darft3 without App UI (WBC 1.0)")
    v2: Optional[ClosedAppView] = Field(default=None, description="App view for EAD v1-darft3 with App UI (WBC 2.0)")
    v3: Optional[ClosedAppView] = Field(default=None, description="App view for EAD v3")


# Portal App


class PostAdminPortalApp(RestrictedBaseModel):
    id: Optional[UUID4] = Field(
        default=None, examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="Portal App ID"
    )
    organization_id: str = Field(
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of the organization providing the portal app"
    )
    status: Optional[ListingStatus] = Field(
        default=None, examples=[ListingStatus.LISTED], description="Listing status of the portal app"
    )
    details: Optional[PostAppDetails] = None
    active_apps: Optional[PostActiveAdminApps] = Field(default=None, description="Active apps for portal app")
    tags: Optional[List[PostAppTag]] = None
    research_only: Optional[bool] = Field(
        examples=[False],
        default=False,
        description="If true, app is intended to be used for reasearch only",
    )
    non_functional: Optional[bool] = Field(
        examples=[False],
        default=False,
        description="If true, portal app can be listed although technical app is not yet available",
    )


class PortalAppCore(RestrictedBaseModel):
    id: UUID4 = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of the portal app")
    organization_id: str = Field(
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of the organization providing the portal app"
    )
    status: ListingStatus = Field(examples=[ListingStatus.DRAFT], descritpion="Status of the app")
    creator_id: str = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="Creator ID")
    created_at: Timestamp = Field(examples=[1598611645], description="UNIX timestamp in seconds - set by server")
    updated_at: Timestamp = Field(examples=[1598611645], description="UNIX timestamp in seconds - set by server")


class PublicPortalApp(PortalAppCore):
    active_app_views: Optional[PublicActiveAppViews] = Field(default=None, description="Currently active app views")


class ClosedPortalApp(PortalAppCore):
    id: UUID4 = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of the portal app")
    active_app_views: Optional[ClosedActiveAppViews] = Field(default=None, description="Currently active app views")


class PublicPortalAppList(RestrictedBaseModel):
    item_count: ItemCount = Field(examples=[123], description="Count of all available apps")
    items: List[PublicPortalApp]


class ClosedPortalAppList(RestrictedBaseModel):
    item_count: ItemCount = Field(examples=[123], description="Count of all available apps")
    items: List[ClosedPortalApp]


# Queries
class BaseQuery(RestrictedBaseModel):
    pass


class PortalAppQuery(BaseQuery):
    active_app_version: Optional[ApiVersion] = Field(
        default=None, examples=[ApiVersion.V3], description="Filter option for active app version"
    )
    tissues: Optional[List[str]] = Field(
        default=None, examples=[["SKIN", "BREAST"]], description="Filter option for tissue types"
    )
    stains: Optional[List[str]] = Field(
        default=None, examples=[["HE", "PHH3"]], description="Filter option for stain types"
    )
    indications: Optional[List[str]] = Field(
        default=None, examples=[["MELANOMA", "PROSTATE_CANCER"]], description="Filter option for indication types"
    )
    analysis: Optional[List[str]] = Field(
        default=None, examples=[["GRADING", "QUANTIFICATION"]], description="Filter option for analysis types"
    )
    clearances: Optional[List[str]] = Field(
        default=None, examples=[["CE_IVD", "CE_IVDR"]], description="Filter option for clearance/certification types"
    )


class CustomerPortalAppQuery(BaseQuery):
    apps: Optional[List[str]] = Field(
        default=None, examples=[["b10648a7-340d-43fc-a2d9-4d91cc86f33f"]], description="List of app IDs"
    )
    tissues: Optional[List[str]] = Field(
        default=None, examples=[["SKIN", "BREAST"]], description="Filter option for tissue types"
    )
    stains: Optional[List[str]] = Field(
        default=None, examples=[["HE", "PHH3"]], description="Filter option for stain types"
    )


class AdminPortalAppQuery(PortalAppQuery, CustomerPortalAppQuery):
    statuses: Optional[List[AppStatus]] = Field(
        default=None, examples=[[AppStatus.DRAFT]], description="Filter option for app status"
    )
    creators: Optional[List[str]] = Field(default=None, examples=[["b10648a7-340d-43fc-a2d9-4d91cc86f33f"]])


class CustomerAppViewQuery(CustomerPortalAppQuery):
    apps: conlist(UUID4, min_length=1) = Field(
        examples=[["b10648a7-340d-43fc-a2d9-4d91cc86f33f"]], description="List of app IDs"
    )
    api_versions: Optional[List[ApiVersion]] = Field(
        default=None, examples=[[ApiVersion.V1]], description="List of supported API versions"
    )


# App Configuratuin


class PostAppConfiguration(RestrictedBaseModel):
    content: ConfigurationModel = Field(
        examples=[{"secret1": "value", "secret2": 100}], description="Dictionary of key-value-pairs"
    )


class AppConfiguration(RestrictedBaseModel):
    app_id: str = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="App ID")
    global_: ConfigurationModel = Field(
        default={},
        examples=[config_section_example],
        description="Global app configuration as dictionary of key-value-pairs",
        alias="global",
    )
    customer: ConfigurationModel = Field(
        default={},
        examples=[config_section_example],
        description="Customer app configuration as dictionary of key-value-pairs",
    )
