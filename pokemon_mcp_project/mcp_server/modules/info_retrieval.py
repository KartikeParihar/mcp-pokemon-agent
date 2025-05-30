import requests
import os
from dotenv import load_dotenv

load_dotenv()
POKEAPI_BASE = os.getenv("POKE_API_URL")

def get_pokemon_info(name):
    url = f"{POKEAPI_BASE}/pokemon/{name.lower()}"
    res = requests.get(url)
    if res.status_code != 200:
        raise ValueError("Pokemon not found")
    data = res.json()
    return {
        'name': data['name'],
        'id': data['id'],
        'height': data['height'],
        'weight': data['weight'],
        'types': [t['type']['name'] for t in data['types']],
        'stats': {s['stat']['name']: s['base_stat'] for s in data['stats']},
        'abilities': [a['ability']['name'] for a in data['abilities']]
    }