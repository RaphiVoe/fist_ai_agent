import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory, file_path)
    if os.path.abspath(working_directory) not in os.path.abspath(path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(path, "r") as f:
            content = f.read(MAX_CHARS)
    except Exception as e:
        return f'Error: Failed to read "{file_path}": {e}'
    return content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the first 10000 characters of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the desired file, relative to the working directory.",
            ),
        },
    ),
)
