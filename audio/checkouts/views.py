from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Cart,Product,Profile,CartItems,ProductVarient
from django.http import HttpResponse
from . models import Address,Coupon
import json
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Profile, Cart, Address, PaymentMethod, Order,OrderItems,Wallet,CartItems
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils import timezone

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
    
    out_of_stock = False
    grand_total = 0
    for cart_item in cart_items:
        sub_total = cart_item.calculate_sub_total()
        grand_total += sub_total
        variant = ProductVarient.objects.get(product = cart_item.product, size = cart_item.size)
        if cart_item.quantity > variant.stock:
            out_of_stock = True

    if request.method == "POST":
        if "submit_cod" in request.POST:
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

            payment_method_id = "COD"
            
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
                
                sub_total = cart_product.quantity * cart_product.product.selling_price

                # Create an order item
                order_item = OrderItems.objects.create(
                    order=order,  
                    product=cart_product.product,
                    quantity=cart_product.quantity,
                    product_price=cart_product.product.selling_price,
                    size = cart_product.size,
                    sub_total=sub_total,
                )

                
                # Calculate the total for the current order item
                
                order_item.save()
                product_stock = ProductVarient.objects.get(product = cart_product.product,size = cart_product.size)
                product_stock.stock -= cart_product.quantity
                product_stock.sold += cart_product.quantity
                product_stock.save()



            order.calculate_bill_amount()

            # Clear the user's cart
            cart_items.delete()

            return render(request, 'checkouts/order_placed.html')
        
    
    context['out_of_stock'] = out_of_stock
    context['products'] = cart_items
    context['grand_total'] = grand_total
    context['user'] = profile
    context['addresses'] = addresses
    request.session['initial_cart_items'] = serialize_cart_items(cart_items)

    return render(request, 'checkouts/checkout.html', context)

def coupon_validation(code):
    try:
        coupon = Coupon.objects.get(code = code)
        current_datetime = timezone.now()
        if coupon.expiry_date >= current_datetime:
            
            return True
        else:
            
            return False
    except:
        return False

def create_order(request):
    if request.method == 'POST':
        address_id = request.POST.get('addressId')
        payment_method = PaymentMethod.objects.get(method="Razor_pay")
        cart_items = CartItems.objects.filter(cart__user=request.user.profile)
        
        wallet_applied = request.POST.get('useWallet')
        coupon_code = request.POST.get('coupon_code', None)
        print(coupon_code)
        valid = coupon_validation(str(coupon_code))
        print(valid)
        order = Order.objects.create(
            user=request.user,
            address=Address.objects.get(uid=address_id),
            payment_method=payment_method,
            
        )

        if valid:
            coupon = Coupon.objects.get(code = coupon_code)
            order.coupon = coupon
            order.save()

        grand_total = 0
        order_items = []
        for cart_item in cart_items:
            sub_total = cart_item.calculate_sub_total()
            grand_total += sub_total


            if valid:
                discounted_subtotal = float(sub_total) * float((100 - float(order.coupon.discount_percentage))/100)
                print(discounted_subtotal)
                order_items.append({
                    'product': cart_item.product,
                    'quantity': cart_item.quantity,
                    'product_price': cart_item.product.selling_price,
                    'size': cart_item.size,
                    'sub_total': sub_total,
                    'discounted_subtotal':discounted_subtotal,

                })
            else:
                order_items.append({
                    'product': cart_item.product,
                    'quantity': cart_item.quantity,
                    'product_price': cart_item.product.selling_price,
                    'size': cart_item.size,
                    'sub_total': sub_total,
                    'discounted_subtotal':sub_total,
                })



        # Create all order items
        OrderItems.objects.bulk_create([
            OrderItems(order=order, **item) for item in order_items
        ])

        
        order.calculate_bill_amount()
        order_items = OrderItems.objects.filter(order = order)
        grand_total = 0
        for item in order_items:
            grand_total += item.discounted_subtotal
        
        # Initialize the Razorpay client
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        order.amount = grand_total
        if wallet_applied == "true":
            wall_amount = request.user.profile.wallet.amount
            order.wallet_applied = True
            if wall_amount < grand_total:
                grand_total -= wall_amount
                order.amount_to_pay = grand_total + 50
            else:
                grand_total = 0
                order.amount_to_pay = 50
                
        
        grand_total_in_paise = int(grand_total * 100)+5000
        
        # Create the Razorpay payment
        payment = client.order.create({'amount': grand_total_in_paise, "currency": "INR", "payment_capture": 1})
        
        order.razor_pay_id = payment['id']
        order.save()
        
        return JsonResponse({'payment': payment}, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def success(request, uid):
    wallet = request.user.profile.wallet
    cart_items = CartItems.objects.filter(cart__user=request.user.profile)
    order = Order.objects.get(uid = uid)
    order_items =OrderItems.objects.filter(order = order)
    for item in order_items:
        varient = ProductVarient.objects.get(product = item.product, size = item.size)
        varient.stock -= item.quantity
        varient.sold += item.quantity
        varient.save()
    if order.wallet_applied == True :
        if wallet.amount > order.bill_amount + 50 :
            wallet.amount -= order.bill_amount
            wallet.save()
        else:
            wallet.amount = 0
            wallet.save()
    cart_items.delete()
    return  render(request, 'checkouts/order_placed.html')

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        
        
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        
        json_data = list(request.POST.keys())[0]

        try:
            data = json.loads(json_data)

            razorpay_payment_id = data.get('paymentData', {}).get('razorpay_payment_id', '')
            razorpay_order_id = data.get('paymentData', {}).get('razorpay_order_id', '')
            razorpay_signature = data.get('paymentData', {}).get('razorpay_signature', '')

            client.utility.verify_payment_signature({
                                                    'razorpay_order_id': razorpay_order_id,
                                                    'razorpay_payment_id': razorpay_payment_id,
                                                    'razorpay_signature': razorpay_signature
                                                    })

            order = Order.objects.get(razor_pay_id = razorpay_order_id)
            order.is_paid = True
            order.save()
            
            return JsonResponse({'id' : order.uid})
       

        except razorpay.errors.SignatureVerificationError as e:
            
            return JsonResponse({'success': False, 'error_message': 'Payment verification failed'})

    return JsonResponse({'success': False, 'error_message': 'Invalid request'})

@csrf_exempt
def update_status(request):
    if request.method == 'POST':
        razorpay_order_id = request.POST.get('razorpay_order_id')
        try:
            order = Order.objects.get(razor_pay_id=razorpay_order_id)
            orders = OrderItems.objects.filter(order = order)
            for item in orders:
                item.status = "Canceled"
                product = ProductVarient.objects.get(product = item.product, size = item.size)
                product.stock += item.quantity
                product.sold -= item.quantity
                product.save()
                item.save()
            # Respond with a success JSON response
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Order not found'})
    return JsonResponse({'success': False, 'error_message': 'Invalid request method'})

def payment_failed(request):
    
    return render(request, 'checkouts/payment_failed.html')

@csrf_exempt
def delete_order(request):
    if request.method == 'POST':
        razorpay_order_id = request.POST.get('razorpay_order_id')
        try:            
            order = Order.objects.get(razor_pay_id=razorpay_order_id)
            order_items = OrderItems.objects.filter(order = order)
            for item in  order_items:
                varient = ProductVarient.objects.get(product = item.product, size = item.size)
                varient.stock += item.quantity
                varient.sold -= item.quantity
                varient.save()
            order.delete()

            return JsonResponse({'success': True})

        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Order not found'})

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'})  
  
def wallet(request):
    wallet_amount = request.user.profile.wallet.amount
    coupon_code = request.POST.get('coupon_code', None)  
    
    current_datetime = datetime.now() 
    grand_total = 0
    order = CartItems.objects.filter(cart__user = request.user.profile)
    for item in order:
        grand_total += (item.quantity * item.product.selling_price)
  
    if float(wallet_amount) < (float(grand_total)):
       amount = float(grand_total + 50) - float(wallet_amount)
       
    else:
        amount = 50
    wallet = wallet_amount if wallet_amount < grand_total else grand_total
    response_data = {'new_order_total': amount,'wallet' : wallet }
    
    if coupon_code:
        coupon = Coupon.objects.get(code = coupon_code)
        current_datetime = timezone.now()
        if coupon.expiry_date >= current_datetime:
            response_data['discount_percent'] = coupon.discount_percentage
            grand_total = float(grand_total) * ((100 - float(coupon.discount_percentage))/100)
            if float(wallet_amount) > grand_total:
                wallet_amount = grand_total 
                amount = 50
            elif float(wallet_amount) < grand_total:
                amount = float(grand_total) - float(wallet_amount) + 50
            response_data['new_order_total'] = amount
            response_data['wallet'] = wallet_amount

    return JsonResponse(response_data)


def validate_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code', None)
        wallet_applied = request.POST.get('useWallet')
        response_data = {}
        
        cart = Cart.objects.get(user = request.user.profile)
        cart_items = CartItems.objects.filter(cart = cart)

        grand_total = 0
        for item in cart_items:
            grand_total += (item.quantity * item.product.selling_price)

        
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                current_datetime = timezone.now()
                if coupon.expiry_date >= current_datetime:
                    response_data['success'] = True
                    response_data['discount_percent'] = coupon.discount_percentage
                    grand_total = float(grand_total) * ((100 - float(coupon.discount_percentage))/100)
                    response_data['total'] = grand_total + 50
                    if wallet_applied == "true":
                        if request.user.profile.wallet.amount > grand_total:
                            wallet_amount = grand_total
                            order_total = 50
                            response_data['wallet'] = wallet_amount
                            response_data['total'] = order_total
                        elif request.user.profile.wallet.amount < grand_total:
                            wallet_amount = request.user.profile.wallet.amount
                            order_total = float(grand_total) - float(wallet_amount) + 50
                            response_data['wallet'] = wallet_amount
                            response_data['total'] = order_total

                else:
                    response_data['success'] = False
                    response_data['message'] = 'Coupon has expired.'
            except Coupon.DoesNotExist:
                response_data['success'] = False
                response_data['message'] = 'Coupon does not exist or is not active.'
        else:
            response_data['success'] = False
            response_data['message'] = 'Invalid coupon code.'

        return JsonResponse(response_data)
    
