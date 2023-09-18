import uuid
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Profile
from django.urls import reverse
from .utils import send_forgot_pass_token

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
    if request.user.is_authenticated and request.user.is_staff is False:
        return redirect('/')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(username = email)
        user_obj = User.objects.get(username = email)
        
        if not user.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        elif not user[0].profile.email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)
        
        elif user[0].profile.is_blocked is True:
            messages.warning(request, 'Your account has been blocked.')
            return HttpResponseRedirect(request.path_info)

        
        elif user and user_obj.is_staff is False and user[0].profile.email_verified:
            user = authenticate(username = email , password= password)
            login(request , user)
            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')


def verify_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
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
        user = Profile.objects.get(forgot_password_token = forgot_password_token)
        

        if request.method == "POST":
            username = request.POST.get('email')
            password = request.POST.get('pass1')
            re_password = request.POST.get('pass2')
            if password == re_password and len(password) < 8:
                messages.warning(request, "Passwords must be minimum of 8 length.")  
            elif password == re_password and len(password)  > 8:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                messages.success(request, "Password changed successfully")
                return redirect('/account/login')



        else:
            context['user_id'] = user.user.username 
            return render(request, 'accounts/forgot_pass.html', context)       
    except Exception as e:

        return HttpResponse(e)
        
