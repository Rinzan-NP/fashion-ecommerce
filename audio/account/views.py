import uuid
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Profile
from django.urls import reverse
from .utils import send_account_activation_email, send_forgot_pass_token
from django.utils import timezone
from datetime import timedelta 

# Create your views here.

def register(request):
    if request.user.is_authenticated and request.user.is_staff is False:
        return redirect('/')
    if request.method == "POST":
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        
        if password == re_password and len(password) < 8:
            messages.warning(request, "Passwords must be minimum of 8 length.")  
        elif password == re_password and len(password)  > 8:
            if User.objects.filter(username=email).exists():
                messages.warning(request, "Email already taken!")
                return HttpResponseRedirect(request.path_info)
            else:
                user = User.objects.create_user(username=email, password=password, email=email, first_name=firstname, last_name=lastname)
                messages.success(request, "An email is sent to your email to verify your email.")
                return HttpResponseRedirect(request.path_info)

                      
        else:
            messages.warning(request, "Passwords do not match .")
            return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/register.html')

def logining(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(username=email).first()

        if not user:
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)

        if not user.profile.email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        if user.profile.is_blocked:
            messages.warning(request, 'Your account has been blocked.')
            return HttpResponseRedirect(request.path_info)

        authenticated_user = authenticate(username=email, password=password)
        
        if authenticated_user is not None and not authenticated_user.is_staff:
            login(request, authenticated_user)
            return redirect('/')
        
        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')

def verify_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        token_expiration = user.email_token_created_at + timedelta(minutes=2)
        if timezone.now() > token_expiration:
            messages.warning(request, "Token has been  expired please try again")
            return redirect(reverse('logining'))
        
        user.email_verified = True
        user.save()
        messages.success(request, 'Your account is  verified.')
        return redirect('/account/login')  # Use the URL pattern name 'login'
    except Profile.DoesNotExist:
        return HttpResponse('Invalid Email token') 

def logouting(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/') 

def verify_account(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(username = email)
        if not user.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
        
        elif not user[0].profile.email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)
        
        elif user is not None and user[0].profile.email_verified:

            # creating a token
            forgot_password_token = str(uuid.uuid4())

            # creating user object and profile object and setting forgoy_pass_token
            user_obj = User.objects.get(username = email)
            profile_obj = Profile.objects.get(user = user_obj)
            profile_obj.forgot_password_token = forgot_password_token
            profile_obj.forgot_password_token_created_at = timezone.now()
            profile_obj.save()
            
            # sending message and mail
            messages.success(request, 'A email is sented to your email!')
            send_forgot_pass_token(email, user_obj.first_name, forgot_password_token)
            return HttpResponseRedirect(request.path_info)
    else:        
        return render(request, 'accounts/verify_account.html')
    
def change_password(request, forgot_password_token):
    context = {}
    try:
        profile = Profile.objects.get(forgot_password_token=forgot_password_token)
        
        token_expiration = profile.forgot_password_token_created_at + timedelta(minutes=2)
        if timezone.now() > token_expiration:
            messages.warning(request, "Forgot password timeout, please try again!")
            return redirect(reverse('logining'))
        else:
            if request.method == "POST":
                new_password = request.POST.get('pass1')
                re_password = request.POST.get('pass2')
                if new_password == re_password and len(new_password) < 8:
                    messages.warning(request, "Passwords must be a minimum of 8 characters.")  
                elif new_password == re_password and len(new_password) >= 8:
                    # Set the new password securely for the associated User
                    user = profile.user
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password changed successfully")
                    return redirect('/account/login')
            else:
                context['user_id'] = profile.user.username
                return render(request, 'accounts/forgot_pass.html', context)       
    except Profile.DoesNotExist:
        messages.warning(request, "Profile not found.")
        return redirect(reverse('logining'))
    except Exception as e:
        return HttpResponse(e)
        
def email_verification(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email = email)
            profile = Profile.objects.get(user = user)
            if profile.email_verified is True:
                messages.success(request,"Email is already verified!")
                return redirect(reverse('logining'))
            else:
                try:
                    profile = Profile.objects.get(user = user)
                    email_token = str(uuid.uuid4())
                    email = user.email
                    profile.email_token = email_token
                    profile.email_token_created_at = timezone.now()
                    profile.save()
                    username = user.first_name
                    
                    send_account_activation_email(email, email_token, username)
                    messages.success(request, "An email has been sended to your account!")
                    return redirect(reverse('logining'))
                except Exception as e:
                    return HttpResponse(e)

        except Exception as e:
            messages.warning(request, "account doesnt exist!")
            return redirect(reverse('verify_email_account'))

    return render(request, 'accounts/verify_email.html')

