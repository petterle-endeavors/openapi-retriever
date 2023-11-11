"""Define the stack for the API."""
from pathlib import Path
from constructs import Construct
from tai_aws_account_bootstrap.base_stack import BaseStack
from tai_aws_account_bootstrap.stack_config_models import StackConfigBaseModel

from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_lambda_python_alpha import (
    PythonFunction,
    PythonLayerVersion,
)


_CURRENT_DIR = Path(__file__).parent
_API_ENTRY_POINT = _CURRENT_DIR.parent / "api"
_TOP_LEVEL_DIR = _CURRENT_DIR.parent.parent


class APIStack(BaseStack):
    """Define the stack for the API."""

    def __init__(
        self,
        scope: Construct,
        config: StackConfigBaseModel,
    ) -> None:
        """Initialize the stack."""
        super().__init__(
            scope=scope,
            config=config,
        )

        self._api = PythonFunction(
            self,
            "api",
            entry=_API_ENTRY_POINT.as_posix(),
            runtime=Runtime.PYTHON_3_10,
            # layers=[
            #     PythonLayerVersion(
            #         self,
            #         "api-dependencies",
            #         entry=_TOP_LEVEL_DIR.as_posix(),
            #         compatible_runtimes=[Runtime.PYTHON_3_10],
            #     )
            # ]
        )
