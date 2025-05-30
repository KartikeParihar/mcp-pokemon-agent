from typing import Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP(name="pokemon", host="0.0.0.0", port=8001)
POKEAPI_BASE = "https://pokeapi.co/api/v2"

async def make_api_request(url: str) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@mcp.tool()
async def get_pokemon_data(name: str) -> str:
    url = f"{POKEAPI_BASE}/pokemon/{name.lower()}"
    data = await make_api_request(url)
    if not data:
        return "Pokemon not found."
    return f"Name: {data['name']}, Types: {[t['type']['name'] for t in data['types']]}"

if __name__ == "__main__":
    mcp.run(transport="sse")