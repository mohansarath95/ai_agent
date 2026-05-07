import os
from xmlrpc import client
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_functions import available_functions
from models import *

def main():
    print("Hello from aiagent!")

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

    model_name = model2s        #MODEL

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    if response.usage_metadata is None:
        raise RuntimeError("API request failed: usage_metadata is missing from the response.")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    print(f"Response:\n{response.text}")

def generate_content(client, messages):
    return client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
    )


if __name__ == "__main__":
    main()
