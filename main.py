import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")

client = genai.Client(api_key=api_key)  # Set up the client with the API key
prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
response = client.models.generate_content(
    model='gemini-2.5-flash', contents=prompt
)
# Verify that usage_metadata is present
if response.usage_metadata is None:
    raise RuntimeError("API request failed: usage_metadata is missing from the response.")
print(f"User prompt: {prompt}")
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(f"Response:\n{response.text}")

def main():
    print("Hello from aiagent!")


if __name__ == "__main__":
    main()
