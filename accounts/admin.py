from django.contrib import admin
from .models import PendingRegistration,Profile
# Register your models here.

admin.site.register(PendingRegistration)
admin.site.register(Profile)
