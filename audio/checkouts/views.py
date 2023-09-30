from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Cart,Product,Profile,CartItems
from django.http import HttpResponse
from . models import Address,Coupon

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile, Cart, Address, PaymentMethod, Order,OrderItems

def checkout(request, user_uid):
    context = {}
    profile = Profile.objects.get(uid=user_uid)
    cart = Cart.objects.get(user=profile)
    cart_items = CartItems.objects.filter(cart__user=profile)
    addresses = Address.objects.filter(unlisted=False, user=request.user)

    if request.method == "POST":
        # Get selected address and payment method from the form
        address_id = request.POST.get('addressId')
        payment_method_id = request.POST.get('payment_method')
        
        # Create a new order
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
            sub_total = cart_product.quantity * cart_product.product.price

            # Create an order item
            order_item = OrderItems.objects.create(
                order=order,  # We'll set this after creating the order
                status="Pending",  # You can set the initial status as needed
                product=cart_product.product,
                quantity=cart_product.quantity,
                product_price=cart_product.product.price,
                sub_total=sub_total,
            )

            # Calculate the total for the current order item
            cart_product.product.stock -= cart_product.quantity
            cart_product.product.save()
            order_item.save()

        order.calculate_bill_amount()


        # Clear the user's cart
        cart_items.delete()

        return redirect(reverse('order_placed'))

    # If it's not a POST request, retrieve data for the checkout page
    context['products'] = cart_items
    context['grand_total'] = cart.total_price
    context['user'] = profile
    context['addresses'] = addresses

    return render(request, 'checkouts/checkout.html', context)

def order_placed(request):
    return render(request, 'checkouts/order_placed.html')

