import os


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
