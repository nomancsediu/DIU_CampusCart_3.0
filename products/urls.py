from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name = 'home'),
    path('sell/', views.sell_view, name = 'sell'),
    path('buy/', views.buy_view, name = 'buy'),
]
