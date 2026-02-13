from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
# Create your models here.

class PendingRegistration(models.Model):
    username = models.CharField(max_length = 150)
    full_name = models.CharField(max_length = 255, blank=True)
    email = models.EmailField(unique = True)
    password_hash = models.CharField(max_length = 128)

    otp_code = models.CharField(max_length = 6)
    created_at = models.DateTimeField(auto_now_add = True)

    def is_expired(self):
        return timezone.now() > self.created_at+timedelta(minutes = 10)
    def __str__(self):
        return f"{self.email} (pending)"
    

# models.py
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=80, blank=True)
    batch = models.CharField(max_length=30, blank=True)  # Fixed spelling

    def __str__(self):
        return f"Profile {self.user.username}"
    