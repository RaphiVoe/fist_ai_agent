import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    print("Hello from fist-ai-agent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 1:
        print("Usage: python3 main.py <prompt>")
        return sys.exit(1)
    user_prompt = sys.argv[1]
    verbose = True if len(sys.argv) > 2 and sys.argv[2] == "--verbose" else False

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents=messages)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose:
        print(f"User prompt: {user_prompt}\n")
    print(response.text)
    if verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
