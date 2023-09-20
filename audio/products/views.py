from django.http import HttpResponse
from django.shortcuts import render,redirect
from account.models import Profile
from .models import Wishlist,Product
# Create your views here.
def wishlist_management(request,user_uid, product_uid):
    try:
        user_obj = Profile.objects.get(uid = user_uid)
        product_obj = Product.objects.get(uid = product_uid)
        if not Wishlist.objects.filter(user = user_obj, product = product_obj).exists():
            Wishlist.objects.create(user = user_obj, product = product_obj)
        else:
            Wishlist.objects.filter(user = user_obj, product = product_obj).delete()
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponse(e)
    
        
