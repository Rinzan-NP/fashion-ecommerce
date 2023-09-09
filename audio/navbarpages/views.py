from django.shortcuts import render,render

# Create your views here.
def home(request):
    return render(request, 'navbarpages/index.html')

