from django.db import models
from base.models import BaseModel
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import functions
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .utils import send_account_activation_email
from django.utils import timezone
from datetime import timedelta 
import random
# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null = True, blank = True)
    profile_image = models.ImageField(
        null=True,
        default="profile/dummy_profile.jpg",  # Relative path to the default image
        upload_to='profile'
    )
    is_blocked = models.BooleanField(default=False)
    forgot_password_token = models.CharField(max_length=100, null = True, blank = True)
    forgot_password_token_created_at = models.DateTimeField(default=timezone.now)
    email_token_created_at = models.DateTimeField(default=timezone.now)
    referance_code = models.CharField(max_length= 12)
    refered = models.CharField(max_length=12,default="",blank=True,null=True)

    def __str__(self) -> str:
        return self.user.username
    
    def generate_reference_code(self):
        while True:
            unique_code = random.randint(1000000, 9999999)  # Generates a 7-digit random number
            if not Profile.objects.filter(referance_code=unique_code).exists():
                self.referance_code = f"REF{unique_code}"
                break
    
    def save(self, *args, **kwargs):
        if not self.referance_code:
            self.generate_reference_code()
        super(Profile, self).save(*args, **kwargs)







@receiver(post_save, sender = User)
def send_email_tokent(sender,  instance, created, **kwargs):
    try:
        if created and instance.is_staff is False:
            email_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = instance, email_token = email_token)
            email = instance.email
            profile_obj.email_token = email_token
            username = instance.first_name
            profile_obj.email_token_created_at = timezone.now()
            
            profile_obj.save()
            send_account_activation_email(email, email_token, username)

    except Exception as e:
        return HttpResponse(e)

