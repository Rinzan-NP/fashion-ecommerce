from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null = True, blank = True)
    profile_image =models.ImageField(upload_to="profile",null=True)
    phone_number = models.IntegerField()

