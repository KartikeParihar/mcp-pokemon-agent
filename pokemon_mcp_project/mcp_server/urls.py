from django.urls import path
from . import views

urlpatterns = [
    path('pokemon/<str:name>/', views.get_pokemon, name='get_pokemon'),
    path('compare/', views.compare_pokemon, name='compare_pokemon'),
    path('strategy/<str:name>/', views.get_strategy, name='get_strategy'),
    path('team/', views.generate_team, name='generate_team'),
]