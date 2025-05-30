from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .modules.info_retrieval import get_pokemon_info
from .modules.compare import PokemonComparer
from .modules.strategy import recommend_counters
from .modules.team_composition import generate_team_with_gemini

logger = logging.getLogger(__name__)

@csrf_exempt
def get_pokemon(request, name):
    try:
        data = get_pokemon_info(name)
        logger.info(f"Retrieved Pokemon: {name}")
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error getting Pokemon {name}: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def compare_pokemon(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name1 = data.get('pokemon1')
            name2 = data.get('pokemon2')
            
            if not name1 or not name2:
                return JsonResponse({'error': 'Both pokemon names are required'}, status=400)
            
            comparer = PokemonComparer(name1, name2)
            result = comparer.compare()
            logger.info(f"AI Compared {name1} vs {name2}")
            return JsonResponse(result)
        except Exception as e:
            logger.error(f"Error comparing Pokemon: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'POST method required'}, status=405)

@csrf_exempt
def get_strategy(request, name):
    try:
        data = recommend_counters(name)
        logger.info(f"Generated strategy for: {name}")
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error getting strategy for {name}: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def generate_team(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            description = data.get('description')
            result = generate_team_with_gemini(description)
            logger.info(f"Generated team for: {description}")
            return JsonResponse(result)
        except Exception as e:
            logger.error(f"Error generating team: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)