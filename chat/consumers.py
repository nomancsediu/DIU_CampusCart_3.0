import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # URL থেকে conversation_id নেওয়া
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        user = self.scope.get("user", AnonymousUser())

        # ইউজার লগইন না থাকলে কানেকশন রিজেক্ট করা
        if user.is_anonymous:
            await self.close()
            return

        # ইউজার এই চ্যাট রুমের মেম্বার কি না তা চেক করা
        allowed = await self.check_user_allowed(user.id, self.conversation_id)
        if not allowed:
            await self.close()
            return

        # গ্রুপে জয়েন করা
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        user = self.scope["user"]
        data = json.loads(text_data)
        content = data.get("message", "").strip()

        if not content:
            return

        # মেসেজ সেভ করা (+ first-email send)
        msg_data = await self.create_message(self.conversation_id, user.id, content)

        # রুমের সবাইকে মেসেজ পাঠানো
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg_data["content"],
                "sender": msg_data["sender"],
                "sender_id": msg_data["sender_id"],
                "created_at": msg_data["created_at"],
            }
        )

    async def chat_message(self, event):
        # ব্রাউজারে ডাটা পুশ করা
        await self.send(text_data=json.dumps(event))

    # --- ডাটাবেজ অপারেশন (Sync to Async) ---

    @database_sync_to_async
    def check_user_allowed(self, user_id, conversation_id):
        try:
            convo = Conversation.objects.get(id=conversation_id)
            # চেক করা যে ইউজার বায়ার অথবা সেলার কি না
            return user_id == convo.buyer_id or user_id == convo.seller_id
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def create_message(self, conversation_id, sender_id, content):
        convo = Conversation.objects.select_related("buyer", "seller", "product").get(id=conversation_id)

        msg = Message.objects.create(
            conversation=convo,
            sender_id=sender_id,
            content=content
        )

        # ----------------------------------------------------
        # ✅ First email notification (per receiver, once only)
        # buyer -> seller (seller_first_email_sent_at)
        # seller -> buyer (buyer_first_email_sent_at)
        # ----------------------------------------------------
        if sender_id == convo.buyer_id:
            receiver = convo.seller
            flag_field = "seller_first_email_sent_at"
        else:
            receiver = convo.buyer
            flag_field = "buyer_first_email_sent_at"

        already_sent = getattr(convo, flag_field, None) is not None

        if (not already_sent) and receiver.email:
            site_url = getattr(settings, "SITE_URL", "http://127.0.0.1:8000")
            chat_link = f"{site_url}/chat/{convo.id}/"

            send_mail(
                subject=f"New message about {convo.product.title} • CampusCart Lite",
                message=(
                    f"You got a new message from {msg.sender.username}.\n\n"
                    f"Message:\n{msg.content}\n\n"
                    f"Open chat: {chat_link}"
                ),
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[receiver.email],
                fail_silently=True,
            )

            setattr(convo, flag_field, timezone.now())
            convo.save(update_fields=[flag_field])
        # ----------------------------------------------------

        return {
            "content": msg.content,
            "sender": msg.sender.username,
            "sender_id": msg.sender_id,
            "created_at": msg.timestamp.strftime("%Y-%m-%d %H:%M") if hasattr(msg, 'timestamp') else "",
        }
