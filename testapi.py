import requests
from openai import OpenAI
import os
import research_api
import json




# Let's code research agent FROM SCRATCH (WITHOUT USING FRAMEWORK)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

print(os.environ.get("OPENROUTER_API_KEY"))


# to verify the model
response = client.chat.completions.create(
    model="google/gemini-2.0-flash-exp:free",
    messages=[
        {
          "role": "user",
          "content": "DO you know MBSE?"
        }
    ],
    extra_body={"reasoning": {"enabled": True}}
)
response1 = response.choices[0].message

print(response1)
