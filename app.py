"""Define the cdk application."""
from aws_cdk import App
from openapi_retriever.iac.stack import APIStack
from openapi_retriever.iac.base_stack_config import (
    StackConfigBaseModel,
    AWSDeploymentSettings,
)


APP = App()


API_STACK = APIStack(
    app=APP,
    config=StackConfigBaseModel(
        stack_name="openapi-retriever",
        stack_id="openapi-retriever",
        description="A tool to retrieve OpenAPI specifications.",
        deployment_settings=AWSDeploymentSettings(),
    ),
)


APP.synth()
