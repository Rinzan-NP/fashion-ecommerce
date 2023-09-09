from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from django.db.models import functions
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .utils import send_account_activation_email

# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null = True, blank = True)
    profile_image =models.ImageField(upload_to="profile",null=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username
    
@receiver(post_save, sender = User)
def send_email_tokent(sender,  instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = instance, email_token = email_token)
            email = instance.email
            profile_obj.email_token = email_token
            username = instance.first_name
            send_account_activation_email(email, email_token, username)

    except Exception as e:
        print(e)
