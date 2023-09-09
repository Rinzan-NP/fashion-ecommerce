from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

def send_account_activation_email(email, email_token, username):
    
    subject = 'Verification'
    message = f"""
Hello {username}
You registered an account on Audio, before being able to use your account you need to verify that this is your email address by clicking here: http://127.0.0.1:8000/account/verify/{email_token}

Kind Regards, Audio"""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail( subject, message, email_from, recipient_list )