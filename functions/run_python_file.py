import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    path = os.path.join(working_directory, file_path)
    if os.path.abspath(working_directory) not in os.path.abspath(path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found.'
    if not path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed_process = subprocess.run(["python3", path] + args, timeout=30, capture_output=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    return (f"STDOUT: {completed_process.stdout.decode('utf-8')}\n"
            f"STDERR: {completed_process.stderr.decode('utf-8')}\n"
            f"{f'Process exited with code {completed_process.returncode}' if completed_process.returncode != 0 else ''}\n"
            f"{'No output produced' if not completed_process.stdout and not completed_process.stderr else ''}")

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified python file with given arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the python file you want to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="The list of arguments to pass to the python execution. If not provided, passes no arguments.",
            ),
        },
    ),
)
