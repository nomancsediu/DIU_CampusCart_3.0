from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Conversation, Message

# Create your views here.

@login_required 
def start_chat(request,product_id):
    product = get_object_or_404(Product,id = product_id)

    if product.seller == request.user:
        return redirect("product_detail",pk = product_id)
    
    convo,_ = Conversation.objects.get_or_create(
        product = product,
        buyer = request.user,
        seller = product.seller
    )

    return redirect("chat_room", conversation_id = convo.id)

@login_required
def chat_room(request,conversation_id):
    convo = get_object_or_404(Conversation,id = conversation_id)

    if request.user not in[convo.buyer,convo.seller]:
        return redirect("home")
    
    chat_messages = Message.objects.filter(conversation=convo).order_by("created_at")

    return render(request, "chat/room.html", {
        "conversation": convo,
        "messages": chat_messages
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).order_by("-updated_at")
    
    return render(request, "chat/inbox.html", {"conversations": conversations})
    
