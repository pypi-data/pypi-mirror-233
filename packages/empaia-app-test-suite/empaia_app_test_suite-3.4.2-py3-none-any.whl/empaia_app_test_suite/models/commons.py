from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RestrictedBaseModel(BaseModel):
    """Abstract Super-class not allowing unknown fields in the **kwargs."""

    model_config = ConfigDict(extra="forbid")


class ServiceStatusEnum(str, Enum):
    OK = "ok"
    FAILURE = "failure"


class ServiceStatus(RestrictedBaseModel):
    status: ServiceStatusEnum = Field(examples=[ServiceStatusEnum.OK.value], description="Status of service")
    version: str = Field(examples=["0.3.7"], description="Version of service")
    message: Optional[str] = Field(
        default=None, examples=["Database offline"], description="Message describing the status further if needed"
    )


class ModelSettings(BaseSettings):
    disable_post_validation: bool = False
    model_config = SettingsConfigDict(env_file=".env", env_prefix="models_")
