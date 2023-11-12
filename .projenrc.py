from projen.python import PythonProject, VenvOptions
from projen import TextFile


AUTHORS = [
    "Jacob Petterle",
]
PROJECT = PythonProject(
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
    venv_options=VenvOptions(envdir=".venv"),
    deps=[
        "aws-cdk-lib",
        "aws-cdk.aws-lambda-python-alpha",
        "mangum",
        "fastapi",
        "tai-aws-account-bootstrap",
        "cowsay"
    ],
    dev_deps=["projen@<=0.72.0"],
)
PROJECT.add_git_ignore("**/cdk.out")

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
\tcdk deploy --all --require-approval never --app "python app.py" --profile dev
"""
MAKEFILE = TextFile(
    PROJECT,
    "Makefile",
    lines=MAKEFILE_CONTENTS.splitlines(),
    committed=True,
    readonly=True,
)
CONFIGURE_GITHUB_CREDS_CONTENTS = """\
#!/bin/bash

# Check if the correct number of parameters are passed
if [ "$#" -ne 2 ]; then
    echo "Usage: ./setupGitCLI.sh [email] [name]"
    exit 1
fi

# Setup git cli with provided email and name
git config --global user.email "$1"
git config --global user.name "$2"
projen
echo "Git has been configured with Email: $1 and Name: $2"
"""
CONFIGURE_GITHUB_CREDS = TextFile(
    PROJECT,
    "configureGitCLI.sh",
    lines=CONFIGURE_GITHUB_CREDS_CONTENTS.splitlines(),
    committed=True,
    readonly=True,
)


PROJECT.synth()
