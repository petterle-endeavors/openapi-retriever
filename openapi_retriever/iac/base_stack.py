"""Define a base stack that provides some nice usability features."""
from aws_cdk import Stack
from constructs import Construct

from .base_stack_config import StackConfigBaseModel


class BaseStack(Stack):
    """Define the base stack for all stacks in the project."""

    def __init__(
        self,
        *,
        scope: Construct,
        config: StackConfigBaseModel,
    ) -> None:
        """Initialize the stack."""
        super().__init__(
            scope=scope,
            id=config.stack_id,
            stack_name=config.stack_name,
            description=config.description,
            env=config.deployment_settings.aws_environment,
            tags=config.tags,
            termination_protection=config.termination_protection,
        )
        self._namer = config.namer
        self._config = config
