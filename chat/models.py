from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here

class Conversation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name = "conversations")
    buyer = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "buyer_conversations")
    seller = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "seller_conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    buyer_first_email_sent_at = models.DateTimeField(null=True, blank=True)
    seller_first_email_sent_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        unique_together = ("product","buyer","seller")

    def __str__(self):
        return f"Conversation({self.product_id} {self.buyer} -> {self.seller})"
    

class Message(models.Model):

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User,on_delete = models.CASCADE, related_name = "sent_messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg({self.sender}: {self.content[:20]})"