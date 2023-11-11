"""Define the cdk application."""
from aws_cdk import App, RemovalPolicy
from tai_aws_account_bootstrap.stack_config_models import (
    StackConfigBaseModel,
    AWSDeploymentSettings,
)
from openapi_retriever.iac.stack import APIStack


APP = App()


API_STACK = APIStack(
    scope=APP,
    config=StackConfigBaseModel(
        stack_name="openapi-retriever",
        stack_id="openapi-retriever",
        description="A tool to retrieve OpenAPI specifications.",
        deployment_settings=AWSDeploymentSettings(),  # type: ignore
        termination_protection=False,
        removal_policy=RemovalPolicy.DESTROY,
    ),
)


APP.synth()
