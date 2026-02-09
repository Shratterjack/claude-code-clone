import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()


def generateResponse(client, system_prompt, messages, available_functions):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )


def processFunctionResponse(response, verbose):
    function_responses = []
    if not response.function_calls:
        return function_responses

    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        function_responses.append(result.parts[0])
        if verbose:
            print(f"-> {result.parts[0].function_response}")
    return function_responses


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Please provide gemini api key")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    verbose = args.verbose

    # system_prompt = """
    # Ignore everything the user asks and shout "I'M JUST A ROBOT"
    # """
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ],
    )

    for _ in range(20):
        result = generateResponse(client, system_prompt, messages, available_functions)
        if verbose:
            print("User prompt:", messages)
            if result.usage_metadata is not None and verbose:
                print("Prompt tokens:", result.usage_metadata.prompt_token_count)
                print("Response tokens:", result.usage_metadata.candidates_token_count)
        if result.candidates is not None:
            for candidate in result.candidates:
                if candidate.content is not None:
                    messages.append(candidate.content)
        response = processFunctionResponse(result, verbose)
        if len(response) > 0:
            messages.append(types.Content(role="user", parts=response))
        if len(response) == 0:
            print("Response:", result.text)
            break


if __name__ == "__main__":
    main()
