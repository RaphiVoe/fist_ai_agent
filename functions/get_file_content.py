import os

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
