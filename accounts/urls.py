from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name = 'register'),
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    # path("register/", views.register_view, name="register"),
    path("verify-email/", views.verify_email_view, name="verify_email"),
    path("resend-code/", views.resend_code_view, name="resend_code"),
]
