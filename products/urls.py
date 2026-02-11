from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name = 'home'),
    path('sell/', views.sell_view, name = 'sell'),
    path('buy/', views.buy_view, name = 'buy'),
    path("product/<int:pk>/", views.product_detail_view, name = "product_detail"),
    path("my_product/",views.my_products_view, name = "my_products_view"),
    path("product/<int:pk>/edit/",views.product_edit_view, name = 'product_edit'),
    path("product/<int:pk>delete/",views.product_delete, name = "product_delete")

]
