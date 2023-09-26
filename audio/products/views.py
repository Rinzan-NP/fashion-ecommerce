from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from account.models import Profile
from .models import Wishlist,Product,Cart
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
    
        
def cart_management(request, user_uid, product_uid):
    try:
        user_obj = Profile.objects.get(uid = user_uid)
        product_obj = Product.objects.get(uid = product_uid)
        if not Cart.objects.filter(user = user_obj, product = product_obj).exists():
            Cart.objects.create(user = user_obj, product = product_obj,quantity = 1)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(reverse('cart_listing'))
    except Exception as e:
        return HttpResponse(e)
    

def cart_deleting(request, uid):
    try:
        cart = Cart.objects.get(uid=uid)
        cart.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    except Cart.DoesNotExist:
        return HttpResponse("Cart not found")
    except Exception as e:
        return HttpResponse(str(e))

def quantity_decreasing(request, uid):
    try:
        cart_obj = Cart.objects.get(uid = uid)
        if cart_obj.quantity > 1:
            new_quantity = cart_obj.quantity - 1
            cart_obj.quantity = new_quantity
            cart_obj.save()
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponse(e)
def quantity_increasing(request,uid):
    try:
        cart_obj = Cart.objects.get(uid = uid)
        product_uid = cart_obj.product.uid
        product = Product.objects.get(uid = product_uid)

        if cart_obj.quantity <=  product.stock:
            new_quantity = cart_obj.quantity + 1
            cart_obj.quantity = new_quantity
            cart_obj.save()
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponse(e)