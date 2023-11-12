"""Define the stack for the API."""
from pathlib import Path
import shutil
import tempfile
from os import chmod
from tai_aws_account_bootstrap.base_stack import BaseStack
from tai_aws_account_bootstrap.stack_config_models import StackConfigBaseModel

from aws_cdk import (
    App,
    DockerImage,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as _lambda_python,
)



_CURRENT_DIR = Path(__file__).parent
_API_ENTRY_POINT = _CURRENT_DIR.parent / "api"
_TOP_LEVEL_DIR = _CURRENT_DIR.parent.parent


class APIStack(BaseStack):
    """Define the stack for the API."""

    def __init__(
        self,
        app: App,
        config: StackConfigBaseModel,
    ) -> None:
        """Initialize the stack."""
        super().__init__(
            scope=app,
            config=config,
        )
        print(str(_API_ENTRY_POINT.resolve()))
        # list the contents of the directory
        print("Contents of api directory:")
        print([x for x in _API_ENTRY_POINT.iterdir()])
        self._api = _lambda_python.PythonFunction(
            self,
            "api",
            entry=str(_API_ENTRY_POINT.resolve()),
            runtime=_lambda.Runtime.PYTHON_3_10,
            index="index.py",
            handler="handler",
            architecture=_lambda.Architecture.ARM_64,
            # layers=[
            #     _lambda_python.PythonLayerVersion(
            #         self,
            #         "api-dependencies",
            #         entry=_TOP_LEVEL_DIR.as_posix(),
            #         compatible_runtimes=[
            #             _lambda.Runtime(
            #                 'python3.10:latest-arm64',
            #                 _lambda.RuntimeFamily.PYTHON,
            #                 bundling_docker_image="public.ecr.aws/sam/build-python3.10:latest-arm64"
            #             ),
            #         ],
            #     )
            # ]
        )
