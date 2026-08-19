import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

print("Key loaded:", bool(api_key))


if not api_key:
    print("Gemini API key not found.")
    raise SystemExit()


try:

    client = genai.Client(
        api_key=api_key
    )

    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input="Say hello in one short sentence.",
        store=False
    )

    print("Gemini response:")
    print(interaction.output_text)


except Exception as error:

    print("Gemini Error:")
    print(error)