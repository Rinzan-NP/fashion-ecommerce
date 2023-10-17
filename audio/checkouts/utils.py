from .models import Order,OrderItems
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

def send_account_activation_email(email, email_token, username):
    
    subject = 'Verification'
    message = f"""
Hello {username}

Kind Regards, Fashion"""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail( subject, message, email_from, recipient_list )