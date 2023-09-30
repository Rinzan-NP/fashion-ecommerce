from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from account.models import Profile
from .models import Wishlist,Product,Cart,CartItems
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
        # Get the user and product objects based on the provided IDs.
        user = Profile.objects.get(uid=user_uid)
        product = Product.objects.get(uid=product_uid)

        # Check if a cart already exists for the user.
        cart, created = Cart.objects.get_or_create(user=user)

        # Check if the product is already in the cart.
        cart_item, item_created = CartItems.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            # If the item already exists in the cart, redirect to the cart listing page for this user.
            return redirect(f'/account/cart/{user.uid}')

        # Calculate the total price of the cart and update it.
        cart.calculate_total_price()

        # Save the changes to the cart.
        cart.save()

        # Return a success indicator or relevant data.
        return redirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        # Handle exceptions (e.g., user or product not found) and return an error message.
        return {'success': False, 'message': str(e)}
    

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
    
    