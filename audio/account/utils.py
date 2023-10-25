from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

def send_account_activation_email(email, email_token, username):
    
    subject = 'Verification'
    message = f"""
Hello {username}
You registered an account on Audio, before being able to use your account you need to verify that this is your email address by clicking here: http://fashionecommerce.shop/account/verify/{email_token}

Kind Regards, Audio"""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail( subject, message, email_from, recipient_list )

def send_forgot_pass_token(email, username, forgot_password_token):
    subject = 'Password Resetting'
    message = f"""
Hello {username}
Trouble signing in?
Resetting your password is easy.

Just press the button below. We’ll have you up and running in no time.

Click on : http://fashionecommerce.shop/account/change_password/{forgot_password_token}

If you did not make this request then please ignore this email.

Kind Regards, Audio"""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail( subject, message, email_from, recipient_list )