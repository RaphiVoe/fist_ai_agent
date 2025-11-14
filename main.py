import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


def main():
    print("Hello from fist-ai-agent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional argument
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)

    if len(sys.argv) < 1:
        print("Usage: python3 main.py <prompt>")
        return sys.exit(1)
    user_prompt = sys.argv[1]
    verbose = True if len(sys.argv) > 2 and sys.argv[2] == "--verbose" else False

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    for i in range(0, 20):
        try:
            response = client.models.generate_content(model="gemini-2.0-flash-001",
                                                      contents=messages, config=config)
            for candidate in response.candidates:
                messages.append(candidate.content)

            #prompt_tokens = response.usage_metadata.prompt_token_count
            #response_tokens = response.usage_metadata.candidates_token_count

            #if verbose:
                #print(f"User prompt: {user_prompt}\n")
            #print(response.text)
            if response.function_calls is None and response.text != "":
                print("Final response:")
                print(response.text)
                break
            for function_call_part in response.function_calls:
                #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                result = call_function(function_call_part, verbose=verbose)
                if result.parts[0].function_response.response is None:
                    raise Exception(result.parts[0].function_response.error)
                result_content = types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=function_call_part.name,
                            response={"result": result},
                        )
                    ],
                )
                messages.append(result_content)
                #if verbose:
                    #print(f"-> {result.parts[0].function_response.response}")

            #if verbose:
                #print(f"Prompt tokens: {prompt_tokens}")
                #print(f"Response tokens: {response_tokens}")
        except Exception as e:
            print(f"Error: {e}")
            break


if __name__ == "__main__":
    main()
