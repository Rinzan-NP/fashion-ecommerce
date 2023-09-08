from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from . import views
from django.http import HttpResponse

# Create your views here.
def register(request):

    return render(request, 'accounts/register.html')
