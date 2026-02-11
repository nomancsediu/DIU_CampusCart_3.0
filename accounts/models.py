from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class PendingRegistration(models.Model):
    username = models.CharField(max_length = 150)
    email = models.EmailField(unique = True)
    password_hash = models.CharField(max_length = 128)

    otp_code = models.CharField(max_length = 6)
    created_at = models.DateTimeField(auto_now_add = True)

    def is_expired(self):
        return timezone.now() > self.created_at+timedelta(minutes = 10)
    def __str__(self):
        return f"{self.email} (pending)"
