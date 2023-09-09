from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from . models import Profile
from django.urls import reverse
# Create your views here.

def register(request):
    if request.user.is_authenticated:
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
            else:
                user = User.objects.create_user(username=email, password=password, email=email, first_name=firstname, last_name=lastname)
                messages.success(request, "An email is sent to your email to verify your email.")
                      
        else:
            messages.warning(request, "Passwords do not match .")
    
    return render(request, 'accounts/register.html')


def logining(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(username = email)

        if not user.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        if not user[0].profile.email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user = authenticate(username = email , password= password)
        if user:
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
        return redirect('/account/login')  # Use the URL pattern name 'login'
    except Profile.DoesNotExist:
        return HttpResponse('Invalid Email token') 


def logouting(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/') 
    

    


