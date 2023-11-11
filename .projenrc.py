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
    poetry=False,
    # deps=[
    #     "aws-cdk-lib@2.106",
    #     "aws-cdk.aws-lambda-python-alpha@^2.101.0a0",
    #     "mangum@^0.17",
    #     "fastapi@^0.104",
    #     "python@^3.10",
    #     "tai-aws-account-bootstrap@>=0.0.1",
    # ],
    venv=True,
    deps=[
        "aws-cdk-lib",
        "aws-cdk.aws-lambda-python-alpha",
        "mangum",
        "fastapi",
        "tai-aws-account-bootstrap",
    ],
    dev_deps=["projen@<=0.72.0"],
)

MAKEFILE_CONTENTS = """\
install:
	pip install projen

synth:
	projen --post false

update-deps:
\tpoetry update

docker-start:
\tsudo systemctl start docker

cdk-deploy-all:
\tcdk deploy --all --require-approval never --app "python app.py"
"""
MAKEFILE = TextFile(
    project,
    "Makefile",
    lines=MAKEFILE_CONTENTS.splitlines(),
    committed=True,
    readonly=True,
)


project.synth()
