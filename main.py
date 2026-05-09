import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_functions import available_functions, call_function
from models import *

MODEL = model2p        #AI MODEL, check models.py

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()  # Now we can access `args.user_prompt`

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)  # Set up the client with the API key
    # Create a message with the user's prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    iteration_limit = 20  # Limit the number of iterations to prevent infinite loops
    for _ in range(iteration_limit):
        response = generate_content(client, messages)
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if response.usage_metadata is None:
            raise RuntimeError("API request failed: usage_metadata is missing from the response.")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
        function_results = []
        if not response.function_calls:
            print(f"Response: {response.text}")
            return
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)
            if not function_call_result.parts:
                raise Exception(f"Function call result is missing parts: {function_call_result}")
            if function_call_result.parts[0].function_response is None:
                raise Exception(f"Function call result is missing function_response: {function_call_result.parts[0]}")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception(f"Function call result is missing response: {function_call_result.parts[0].function_response}")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=function_results))
    print("Reached iteration limit without a final response. Ending conversation.")

def generate_content(client, messages):
    global MODEL
    return client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
if __name__ == "__main__":
    main()
