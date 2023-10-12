from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from account.models import Profile
from .models import Wishlist,Product,Cart,CartItems,Size,ProductVarient
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from account.decarator import login_required

# Create your views here.
@login_required
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
    
        
@login_required
def add_to_cart(request, product_uid, size_id):
    try:
        product_obj = Product.objects.get(uid=product_uid)
        size = Size.objects.get(id=size_id)
        product_varient = ProductVarient.objects.get(product =product_obj,size = size)
        cart, created = Cart.objects.get_or_create(user=request.user.profile)

        if product_varient.stock <= 1:
            messages.warning(request, "Out of stock")
            return redirect(request.META.get('HTTP_REFERER'))
        # Check if the item already exists in the cart
        cart_item, item_created = CartItems.objects.get_or_create(cart=cart, product=product_obj, size=size)
        
        
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

@login_required
def cart_deleting(request, uid):
    try:
        cart = CartItems.objects.get(uid=uid)
        cart.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    except Cart.DoesNotExist:
        return HttpResponse("Cart not found")
    except Exception as e:
        return HttpResponse(str(e))

@login_required
def quantity_decreasing(request, uid, product_uid):
    try:
        cart_obj = CartItems.objects.get(uid=uid)
        product = Product.objects.get(uid = product_uid)
        cart = Cart.objects.get(user=request.user.profile)
        cart_objs = CartItems.objects.filter(cart=cart)
        if cart_obj.quantity > 1:
            cart_obj.quantity -= 1
            cart_obj.save()
            subTotal = cart_obj.calculate_sub_total()

        grand_total = 0  # Initialize grand_total outside the loop
        for cart_item in cart_objs:
            sub_total = cart_item.calculate_sub_total()
            grand_total += sub_total  # Accumulate subtotals

        # Return updated data as JSON response after the loop
        response_data = {
            'quantity': cart_obj.quantity,
            'subTotal': subTotal,
            'grandTotal': grand_total,  # Include the correct grand_total value
        }
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e)})

@login_required
def quantity_increasing(request, uid, product_uid):
    try:
        cart_obj = CartItems.objects.get(uid=uid)
        product = Product.objects.get(uid = product_uid)
        size_stock = ProductVarient.objects.get(size=cart_obj.size, product = product)
        cart = Cart.objects.get(user=request.user.profile)
        cart_objs = CartItems.objects.filter(cart=cart)

        if cart_obj.quantity < size_stock.stock:
            cart_obj.quantity += 1
            cart_obj.save()

        grand_total = 0  # Initialize grand_total outside the loop
        for cart_item in cart_objs:
            sub_total = cart_item.calculate_sub_total()
            grand_total += sub_total  # Accumulate subtotals

        # Return updated data as JSON response after the loop
        response_data = {
            'quantity': cart_obj.quantity,
            'subTotal': cart_obj.calculate_sub_total(),  # Calculate subTotal for the updated cart_obj
            'grandTotal': grand_total,  # Include the correct grand_total value
        }
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e)})


    
    