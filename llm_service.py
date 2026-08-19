import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Load .env from this project folder
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)


def generate_llm_reason(data, recommendation):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Gemini API key not found")

        return {
            "reason": recommendation["reason"],
            "llm_used": False
        }

    try:

        client = genai.Client(
            api_key=api_key
        )

        prompt = f"""
You are an Ad Tech optimization assistant.

User behavior:

Scroll depth: {data.scroll_depth}%
Time on page: {data.time_on_page} seconds
Device type: {data.device_type}
Page type: {data.page_type}

The optimization engine selected:

Recommended position:
{recommendation["recommended_position"]}

Ad format:
{recommendation["ad_format"]}

Predicted viewability:
{recommendation["predicted_viewability"]}

Estimated RPM:
{recommendation["estimated_rpm"]}

Explain in one short sentence why this advertisement placement
is suitable for this user's behavior.

Do not change the recommended position.
Do not change the ad format.
Do not change the RPM value.
"""

        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=prompt,
            store=False
        )

        generated_reason = interaction.output_text

        print("Gemini response:", generated_reason)

        return {
            "reason": generated_reason,
            "llm_used": True
        }

    except Exception as error:

        print("Gemini Error:", error)

        return {
            "reason": recommendation["reason"],
            "llm_used": False
        }