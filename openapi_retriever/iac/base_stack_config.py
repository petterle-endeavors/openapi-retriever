"""Define the base stack for all stacks in the project.""" ""
import getpass
import json
from enum import Enum
from typing import Dict, Optional, Set

import boto3
from aws_cdk import Environment, RemovalPolicy
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AWSRegion(str, Enum):
    """Define AWS regions."""

    US_EAST_1 = "us-east-1"
    US_EAST_2 = "us-east-2"
    US_WEST_1 = "us-west-1"
    US_WEST_2 = "us-west-2"


class DeploymentEnvironment(str, Enum):
    """Define deployment environments."""

    Development = "development"
    Production = "production"


class AWSDeploymentSettings(BaseSettings):
    """Define AWS deployment settings."""

    model_config = SettingsConfigDict(env_file="../../.env")

    aws_region: AWSRegion = Field(
        default=AWSRegion.US_EAST_1,
        description="The AWS region to deploy to.",
    )
    deployment_environment: DeploymentEnvironment = Field(
        default=DeploymentEnvironment.Development,
        description="The deployment type. This is used to isolate stacks from various environments.",
    )
    vpc_name: Optional[str] = Field(
        default="account-bootstrap-vpc",
        description="The VPC name to use for deployments.",
    )
    stack_prefix: Optional[str] = Field(default=None, description="Prefix for stack resource names.")

    @property
    def aws_account_id(self) -> str:
        """Get AWS account id."""
        session = boto3.Session()
        return session.client("sts").get_caller_identity()["Account"]

    @property
    def aws_environment(self) -> Environment:
        """Get the CDK environment dict for this app."""
        return Environment(
            account=self.aws_account_id,
            region=self.aws_region,
        )


def generate_resource_name(deployment_settings: AWSDeploymentSettings, name: str) -> str:
    """Resource namer. Use this for naming all named resources."""
    if deployment_settings.stack_prefix:
        return f"{deployment_settings.stack_prefix}-{name}"
    return name


class StackConfigBaseModel(BaseModel):
    """Define the base model for stack configuration."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    deployment_settings: AWSDeploymentSettings = Field(
        ...,
        description="The AWS deployment settings.",
    )
    stack_id: str = Field(
        ...,
        description="The ID of the stack.",
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=255,
        description="The description of the stack.",
    )
    stack_name: str = Field(
        ...,
        description="The name of the stack/service.",
    )

    @property
    def is_prod(self) -> bool:
        """Returns true if this is production environment, otherwise false."""
        return self.deployment_settings.deployment_environment == DeploymentEnvironment.Production

    @property
    def removal_policy(self) -> RemovalPolicy:
        """Returns the stack removal policy."""
        return RemovalPolicy.RETAIN if self.is_prod else RemovalPolicy.DESTROY

    @property
    def termination_protection(self) -> bool:
        """Returns the stack termination protection."""
        return self.is_prod

    @property
    def tags(self) -> Dict[str, str]:
        """Returns stack default tags."""
        return {
            "ben:ai:user": getpass.getuser(),
            "ben:ai:stack-name": self.stack_name,
        }

    def namer(self, name: str) -> str:
        """Resource namer. Use this for naming all named resources."""
        return generate_resource_name(self.deployment_settings, name)

    @model_validator(mode="after")
    def validate_model(self) -> "StackConfigBaseModel":
        """Update the stack name with the stack prefix."""
        self.stack_name = self.namer(self.stack_name)
        return self


def model_dump_runtime_settings(
    settings: BaseSettings,
    *,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    round_trip: bool = False,
    warnings: bool = True,
    exclude: Optional[Set[str]] = None,
) -> Dict[str, str]:
    """Dump the settings model as a serialized python dict."""
    model_dict = settings.model_dump(
        mode="json",
        exclude=exclude,
        by_alias=True,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=True,
        round_trip=round_trip,
        warnings=warnings,
    )
    for key, value in model_dict.items():
        if not isinstance(value, str):
            model_dict[key] = json.dumps(value)
    model_dict = {key.upper(): value for key, value in model_dict.items()}

    try:
        env_prefix = settings.model_config["env_prefix"]
        model_dict = {f"{env_prefix}{key}": value for key, value in model_dict.items()}
    except KeyError:
        pass
    return model_dict
