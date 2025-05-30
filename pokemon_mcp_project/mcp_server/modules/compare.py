import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

import re

def extract_json_from_text(text):
    # Find JSON inside code block or regular text
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            return None
    return None


class PokemonComparer:
    def __init__(self, name1, name2):
        self.name1 = name1.lower()
        self.name2 = name2.lower()

    def compare(self):
        prompt = f"""Compare these two Pokemon: {self.name1} vs {self.name2}

Provide a detailed comparison and return ONLY valid JSON with this structure:
{{
    "pokemon_1": "{self.name1}",
    "pokemon_2": "{self.name2}",
    "winner": "pokemon name or tie",
    "comparison_summary": "detailed comparison explanation",
    "stat_analysis": "which pokemon has better stats overall and why",
    "type_advantage": "type matchup analysis and advantages",
    "recommendation": "which to choose and detailed reasoning"
}}"""

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        
        
        try:
            result = extract_json_from_text(response.text)
            return result
        except:
            return {
                "pokemon_1": self.name1,
                "pokemon_2": self.name2,
                "winner": "analysis failed",
                "comparison_summary": response.text,
                "stat_analysis": "Could not analyze",
                "type_advantage": "Could not determine",
                "recommendation": "Manual comparison needed"
            }
