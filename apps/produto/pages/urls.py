from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('cardapio/', views.Cardapio, name='cardapio'),
]
