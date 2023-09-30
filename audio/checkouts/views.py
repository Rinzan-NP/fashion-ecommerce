from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Cart,Product,Profile,CartItems
from django.http import HttpResponse
from . models import Address,Coupon

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile, Cart, Address, PaymentMethod, Order

def checkout(request, user_uid):
    context = {}
    profile = Profile.objects.get(uid=user_uid)
    cart = Cart.objects.get(user = profile)
    cart_objs = CartItems.objects.filter(cart__user = user_uid)
    addresses = Address.objects.filter(unlisted=False, user=request.user)
   
    if request.method == "POST":
        # Get user profile and cart items
       
        
        # Get selected address and payment method from the form
        address_id = request.POST.get('addressId')
        payment_method = request.POST.get('payment_method')
        
        # Create a new order
        coupon = Coupon.objects.get(code = "123")
        selected_address = Address.objects.get(uid=address_id)
        for cart_product in cart_objs:
            order = Order.objects.create(
                user = request.user,
                address=selected_address,
                payment_method=PaymentMethod.objects.get(method=payment_method),
                status="Pending",  # You can set the initial status as per your requirements
                product= cart_product.product,  
                quantity=cart_product.quantity,
                coupon=coupon,  # You can add coupon logic here if needed
                price=cart_product.total_price,
                amount_to_pay=cart_product.total_price,
            )
            
            # Save the order to the database
            order.save()
            new_stock = cart_product.product.stock - cart_product.quantity
            cart_product.product.stock = new_stock
            cart_product.product.save()
        # Clear the user's cart
        cart_objs.delete()

        return redirect(reverse('order_placed'))
        
        
        # If it's not a POST request, retrieve data for the checkout page

    context['products'] = cart_objs
    context['grand_total'] = cart.total_price
    context['user'] = profile
    context['addresses'] = addresses
    
        
    
    
    return render(request, 'checkouts/checkout.html', context)

def order_placed(request):
    return render(request, 'checkouts/order_placed.html')

