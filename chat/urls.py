from django.urls import path
from . import views

urlpatterns = [
    path("inbox/", views.inbox, name="inbox"),
    path("chat/start/<int:product_id>/", views.start_chat, name="start_chat"),
    path("chat/<int:conversation_id>/", views.chat_room, name="chat_room"),
]