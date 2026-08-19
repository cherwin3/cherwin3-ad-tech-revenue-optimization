import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from google import genai


# Location of the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Location of Cherwin_project/.env
ENV_PATH = PROJECT_ROOT / ".env"

# Load environment variables
load_dotenv(dotenv_path=ENV_PATH, override=True)


def generate_llm_reason(
    position: str,
    ad_format: str,
    scroll_depth: float,
    time_on_page: float,
    viewability: float
) -> Optional[str]:

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print(f"Gemini API key not found in: {ENV_PATH}")
        return None

    # Use the same model as your old working code
    model_name = "gemini-3.7-flash"

    try:
        print("Using Gemini model:", model_name)

        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an Ad Tech optimization assistant.

User behaviour:

Scroll depth: {scroll_depth}%
Time on page: {time_on_page} seconds

The optimization engine selected:

Recommended position: {position}
Ad format: {ad_format}
Predicted viewability: {viewability}

Explain in one short sentence why this advertisement placement
is suitable for this user's behaviour.

Do not change the recommended position.
Do not change the ad format.
Do not change the predicted viewability.
Do not include headings.
"""

        interaction = client.interactions.create(
            model=model_name,
            input=prompt,
            store=False
        )

        generated_reason = interaction.output_text

        if generated_reason:
            generated_reason = generated_reason.strip()

            print("Gemini response:", generated_reason)

            return generated_reason

        print("Gemini returned an empty response")
        return None

    except Exception as error:
        print("Gemini error:", error)
        return None