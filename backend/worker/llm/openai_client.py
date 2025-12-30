import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_summary(transcript: str):
    prompt = f"""
You are an AI meeting assistant.

From the transcript below:
1. Create a short summary
2. Extract decisions
3. Extract clear action items

Return STRICT JSON in this format:

{{
  "summary": "",
  "decisions": [],
  "action_items": [
    {{
      "title": "",
      "description": "",
      "owner": "",
      "priority": "Low|Medium|High"
    }}
  ]
}}

Transcript:
\"\"\"
{transcript}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful meeting assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
