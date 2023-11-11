from projen.python import PythonProject

project = PythonProject(
    author_email="jacobpetterle@gmail.com",
    author_name="Jacob Petterle",
    module_name="openapi_retriever",
    name="openapi-retriever",
    version="0.1.0",
)

project.synth()