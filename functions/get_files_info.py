import os


def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    if os.path.abspath(working_directory) not in os.path.abspath(path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    files = os.listdir(path)
    files_string = ""
    for file in files:
        try:
            file_name = file
            file_size = os.path.getsize(os.path.join(path, file))
            file_is_directory = os.path.isdir(os.path.join(path, file))
            files_string += f'- {file_name}: file_size={file_size} bytes, is_dir={file_is_directory}\n'
        except Exception as e:
            return f'Error: Failed to get info for "{file}": {e}'
    return files_string
