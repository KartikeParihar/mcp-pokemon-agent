import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def extract_json_from_text(text: str):
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            return None
    return None

def generate_team_with_gemini(description: str) -> dict:
    prompt = f"""
You are a Pokemon team builder.

Given this description:
\"\"\"{description}\"\"\"

Please respond ONLY in valid JSON format with two keys:
- 'description': a natural language description explaining the team strategy
- 'team': a list of six Pokemon objects, each with 'name' and 'role' fields

Example:
{{
    "description": "This is a balanced team featuring strong defense and a fire-type attacker.",
    "team": [
        {{"name": "Charizard", "role": "Fire Attacker"}},
        {{"name": "Snorlax", "role": "Tank"}},
        {{"name": "Alakazam", "role": "Special Sweeper"}},
        {{"name": "Golem", "role": "Physical Wall"}},
        {{"name": "Lapras", "role": "Water Support"}},
        {{"name": "Crobat", "role": "Speed Lead"}}
    ]
}}
"""

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    raw_text = response.text

    try:
        team_data = json.loads(raw_text)
    except json.JSONDecodeError:
        team_data = extract_json_from_text(raw_text)

    if not team_data:
        raise ValueError(f"Failed to parse JSON from Gemini response. Raw response: {raw_text}")
    
    return team_data