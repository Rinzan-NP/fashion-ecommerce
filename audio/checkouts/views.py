from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Cart,Product,Profile,CartItems,ProductVarient
from django.http import HttpResponse
from . models import Address,Coupon
import json
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Profile, Cart, Address, PaymentMethod, Order,OrderItems

def serialize_cart_items(cart_items):
    serialized_items = []
    for cart_item in cart_items:
        serialized_item = {
            'product_id': cart_item.product.name,
            'quantity': cart_item.quantity,
            'size': cart_item.size.size,
        }
        serialized_items.append(serialized_item)
    return serialized_items

def compare_cart_items(initial_cart_items, current_cart_items):
    return initial_cart_items == serialize_cart_items(current_cart_items)

def checkout(request, user_uid):
    context = {}
    profile = Profile.objects.get(uid=user_uid)
    cart = Cart.objects.get(user=profile)
    cart_items = CartItems.objects.filter(cart__user=profile)
    addresses = Address.objects.filter(unlisted=False, user=request.user)
    
    grand_total = 0
    for cart_item in cart_items:
        sub_total = cart_item.calculate_sub_total()
        grand_total += sub_total

    if request.method == "POST":
        # Get selected address and payment method from the form
        initial_cart_items = request.session.get('initial_cart_items', [])
        
        if not compare_cart_items(initial_cart_items, cart_items):
            context['cart_changed'] = True
            # For example, you can redirect back to the checkout page with an error message
            context['error_message'] = "Cart items have changed. Please review your order."
            context['products'] = cart_items
            context['grand_total'] = grand_total
            context['user'] = profile
            context['addresses'] = addresses
            return render(request, 'checkouts/checkout.html', context)

        payment_method_id = request.POST.get('payment_method')
        if payment_method_id == "Razor_pay":
            return redirect('payment')
        
        # Create a new order
        address_id = request.POST.get('addressId')
        selected_address = Address.objects.get(uid=address_id)
        payment_method = PaymentMethod.objects.get(method=payment_method_id)

        order = Order.objects.create(
            user=request.user,
            address=selected_address,
            payment_method=payment_method,
            # You can adjust this as needed
        )

        

        for cart_product in cart_items:
            # Calculate the sub-total for the order item
            sub_total = cart_product.quantity * cart_product.product.selling_price

            # Create an order item
            order_item = OrderItems.objects.create(
                order=order,  # We'll set this after creating the order
                 # You can set the initial status as needed
                product=cart_product.product,
                quantity=cart_product.quantity,
                product_price=cart_product.product.selling_price,
                size = cart_product.size,
                sub_total=sub_total,
            )

            # Calculate the total for the current order item
            product_varient = ProductVarient.objects.get(product = cart_product.product, size = cart_product.size,)
            product_varient.stock -= cart_item.quantity
            product_varient.save()
            order_item.save()

        order.calculate_bill_amount()


        # Clear the user's cart
        cart_items.delete()

        return redirect(reverse('order_placed'))

    # If it's not a POST request, retrieve data for the checkout page
    context['products'] = cart_items
    context['grand_total'] = grand_total
    context['user'] = profile
    context['addresses'] = addresses
    request.session['initial_cart_items'] = serialize_cart_items(cart_items)

    return render(request, 'checkouts/checkout.html', context)

def order_placed(request):
    return render(request, 'checkouts/order_placed.html')


def payment(request):
    return render(request, 'checkouts/payment.html')