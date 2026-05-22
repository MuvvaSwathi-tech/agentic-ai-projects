import os

from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("Available Models:")
print("=" * 50)

for model in genai.list_models():
    print(f"Name: {model.name}")
    print(f"Display Name: {model.display_name}")
    print(f"Description: {model.description}")
    print(f"Input Token Limit: {model.input_token_limit}")
    print(f"Output Token Limit: {model.output_token_limit}")
    print("-" * 50)
