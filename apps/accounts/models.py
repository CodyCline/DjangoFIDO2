from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    # Extends built-in user
    phone_num = models.CharField(max_length=12)

class Authenticator(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="keys", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    key_hash = models.CharField(max_length=5000) #Stores the crypto token
    last_used = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

