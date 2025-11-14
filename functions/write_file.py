import os
from google.genai import types


def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)
    if os.path.abspath(working_directory) not in os.path.abspath(path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        except Exception as e:
            return f'Error: Failed to create directory "{os.path.dirname(path)}": {e}'
    try:
        with open(path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error: Failed to write to "{file_path}": {e}'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file path. Overwrites file if it already exists, otherwise creates a new file. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write the content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write.",
            ),
        },
    ),
)
