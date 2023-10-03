from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from account.models import Profile
from .models import Wishlist,Product,Cart,CartItems,Size,ProductVarient
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404

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
    
        

def add_to_cart(request, product_uid, size_id):
    try:
        product_obj = Product.objects.get(uid=product_uid)
        size = Size.objects.get(id=size_id)

        cart, created = Cart.objects.get_or_create(user=request.user.profile)

        # Check if the item already exists in the cart
        cart_item, item_created = CartItems.objects.get_or_create(cart=cart, product=product_obj, size=size)
        product_varient = ProductVarient.objects.get(product =product_obj,size = size)
        print(product_varient.stock)
        if not item_created:
            # If the item already exists, increment the quantity
            if cart_item.quantity < product_varient.stock:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, "Added to cart")
            else:
                messages.warning(request, "Out of stock")

        
        return redirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        return HttpResponse(e)

def cart_deleting(request, uid):
    try:
        cart = CartItems.objects.get(uid=uid)
        cart.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    except Cart.DoesNotExist:
        return HttpResponse("Cart not found")
    except Exception as e:
        return HttpResponse(str(e))

def quantity_decreasing(request, uid):
    try:
        cart_obj = CartItems.objects.get(uid = uid)
        if cart_obj.quantity > 1 :
            cart_obj.quantity -= 1
            cart_obj.save()
            cart_obj.cart.calculate_total_price()
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponse(e)
    
def quantity_increasing(request,uid):
    try:
        cart_obj = CartItems.objects.get(uid = uid)
        if cart_obj.quantity <  cart_obj.product.stock :
            cart_obj.quantity += 1
            cart_obj.save()
            cart_obj.cart.calculate_total_price()
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponse(e)
    
    