from projen.python import PythonProject
from projen import TextFile


AUTHORS = [
    "Jacob Petterle",
]
project = PythonProject(
    author_email="jacobpetterle@tai-tutor.team",
    author_name=AUTHORS[0],
    module_name="openapi_retriever",
    name="openapi-retriever",
    version="0.0.0",
    description="A tool to retrieve OpenAPI specifications.",
    poetry=True,
    deps=[
        "aws-cdk-lib@~2.106",
        "aws-cdk.aws-lambda-python",
    ],
    dev_deps=["projen@<=0.72.20"],
)

MAKEFILE_CONTENTS = """\
install:
	pip install projen

synth:
	projen --post false

update-deps:
	poetry update
"""
MAKEFILE = TextFile(
    project,
    "Makefile",
    lines=MAKEFILE_CONTENTS.splitlines(),
    committed=True,
    readonly=True,
)


project.synth()
