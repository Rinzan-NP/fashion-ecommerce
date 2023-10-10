import uuid
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Profile
from products.models import ProductVarient, Review, Wishlist,Cart,CartItems
from django.urls import reverse
from .utils import send_account_activation_email, send_forgot_pass_token
from django.utils import timezone
from datetime import timedelta 
import os
from django.conf import settings
from checkouts.models import Address,OrderItems,Order,Wallet
from django.shortcuts import get_object_or_404

# Create your views here.

def register(request):
    if request.user.is_authenticated and request.user.is_staff is False:
        return redirect('/')
    if request.method == "POST":
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        
        if password == re_password and len(password) < 8:
            messages.warning(request, "Passwords must be minimum of 8 length.")  
        elif password == re_password and len(password)  > 8:
            if User.objects.filter(username=email).exists():
                messages.warning(request, "Email already taken!")
                return HttpResponseRedirect(request.path_info)
            else:
                user = User.objects.create_user(username=email, password=password, email=email, first_name=firstname, last_name=lastname)
                messages.success(request, "An email is sent to your email to verify your email.")
                return HttpResponseRedirect(request.path_info)

                      
        else:
            messages.warning(request, "Passwords do not match .")
            return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/register.html')

def logining(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(username=email).first()

        if not user:
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)

        if not user.profile.email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        if user.profile.is_blocked:
            messages.warning(request, 'Your account has been blocked.')
            return HttpResponseRedirect(request.path_info)

        authenticated_user = authenticate(username=email, password=password)
        
        if authenticated_user is not None and not authenticated_user.is_staff:
            login(request, authenticated_user)
            return redirect('/')
        
        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')

def verify_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        token_expiration = user.email_token_created_at + timedelta(minutes=2)
        if timezone.now() > token_expiration:
            messages.warning(request, "Token has been  expired please try again")
            return redirect(reverse('logining'))
        
        user.email_verified = True
        user.save()
        messages.success(request, 'Your account is  verified.')
        return redirect('/account/login')  # Use the URL pattern name 'login'
    except Profile.DoesNotExist:
        return HttpResponse('Invalid Email token') 

def logouting(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/') 

def verify_account(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(username = email)
        if not user.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
        
        elif not user[0].profile.email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)
        
        elif user is not None and user[0].profile.email_verified:

            # creating a token
            forgot_password_token = str(uuid.uuid4())

            # creating user object and profile object and setting forgoy_pass_token
            user_obj = User.objects.get(username = email)
            profile_obj = Profile.objects.get(user = user_obj)
            profile_obj.forgot_password_token = forgot_password_token
            profile_obj.forgot_password_token_created_at = timezone.now()
            profile_obj.save()
            
            # sending message and mail
            messages.success(request, 'A email is sented to your email!')
            send_forgot_pass_token(email, user_obj.first_name, forgot_password_token)
            return HttpResponseRedirect(request.path_info)
    else:        
        return render(request, 'accounts/verify_account.html')
    
def change_password(request, forgot_password_token):
    context = {}
    try:
        profile = Profile.objects.get(forgot_password_token=forgot_password_token)
        
        token_expiration = profile.forgot_password_token_created_at + timedelta(minutes=2)
        if timezone.now() > token_expiration:
            messages.warning(request, "Forgot password timeout, please try again!")
            return redirect(reverse('logining'))
        else:
            if request.method == "POST":
                new_password = request.POST.get('pass1')
                re_password = request.POST.get('pass2')
                if new_password == re_password and len(new_password) < 8:
                    messages.warning(request, "Passwords must be a minimum of 8 characters.")  
                elif new_password == re_password and len(new_password) >= 8:
                    # Set the new password securely for the associated User
                    user = profile.user
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password changed successfully")
                    return redirect('/account/login')
            else:
                context['user_id'] = profile.user.username
                return render(request, 'accounts/forgot_pass.html', context)       
    except Profile.DoesNotExist:
        messages.warning(request, "Profile not found.")
        return redirect(reverse('logining'))
    except Exception as e:
        return HttpResponse(e)
        
def email_verification(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email = email)
            profile = Profile.objects.get(user = user)
            if profile.email_verified is True:
                messages.success(request,"Email is already verified!")
                return redirect(reverse('logining'))
            else:
                try:
                    profile = Profile.objects.get(user = user)
                    email_token = str(uuid.uuid4())
                    email = user.email
                    profile.email_token = email_token
                    profile.email_token_created_at = timezone.now()
                    profile.save()
                    username = user.first_name
                    
                    send_account_activation_email(email, email_token, username)
                    messages.success(request, "An email has been sended to your account!")
                    return redirect(reverse('logining'))
                except Exception as e:
                    return HttpResponse(e)

        except Exception as e:
            messages.warning(request, "account doesnt exist!")
            return redirect(reverse('verify_email_account'))

    return render(request, 'accounts/verify_email.html')

def wishlist_listing(request, uid):
    context = {}
    try:
        profile = Profile.objects.get(uid = uid)
        wishlist_products = Wishlist.objects.filter(user = profile)
        context['user'] = profile
        context['products'] = wishlist_products
    except Exception as e:
        return HttpResponse(e)
    return render(request, 'accounts/wishlist.html',context)

def cart_listing(request, uid):
    context = {}
    try:
        # Get the user profile using the provided uid.
        profile = get_object_or_404(Profile, uid=uid)

        # Try to retrieve the user's cart, create one if it doesn't exist.
        cart, created = Cart.objects.get_or_create(user=profile)

        # Retrieve the cart items associated with the user's cart.
        cart_items = CartItems.objects.filter(cart=cart).order_by("-created_at")

        # Calculate the grand total of the cart items.
        

        # Check if any of the products are out of stock.
        out_of_stock = any(
            item.quantity > ProductVarient.objects.get(product=item.product, size=item.size).stock
            for item in cart_items
        )
        grand_total = 0
        for cart_item in cart_items:
            sub_total = cart_item.calculate_sub_total()
            grand_total += sub_total

        context['out_of_stock'] = out_of_stock
        context['grand_total'] = grand_total
        context['user'] = profile
        context['products'] = cart_items
    except Exception as e:
        return HttpResponse(e)
    return render(request, 'accounts/cart.html', context)

def profile(request, uid):
    context = {}
    profile = Profile.objects.get(uid=uid)
    wallet, created = Wallet.objects.get_or_create(user=request.user.profile)
    

    context['profiles'] = profile
    context['wallet'] = wallet
    return render(request, 'accounts/profile/profile.html', context)

def order_listing(request, user_uid):
    context = {}
    profile = Profile.objects.get(uid = user_uid)
    orders = OrderItems.objects.filter(order__user=request.user).order_by('-created_at')
    context['profiles'] = profile
    context['orders'] = orders
    return render(request, 'accounts/profile/orders.html',context)

def order_detail(request, order_uid):
    context = {}
    order = OrderItems.objects.get(uid = order_uid)
    if request.method == "POST":
        review = request.POST.get('review')
        user_review = Review.objects.get(user = request.user.profile, product = order.product)
        user_review.review = review
        user_review.save()
        return redirect(request.META.get('HTTP_REFERER'))

    context['order'] = order
    try:
        context['review'] = Review.objects.get(user = request.user.profile, product = order.product)
    except:
        Review.objects.create(user = request.user.profile, product = order.product, review = "")
        context['review'] = Review.objects.get(user = request.user.profile, product = order.product)
    return render(request, 'accounts/profile/order_detail.html', context)

def order_canceling(request, order_uid):
    try:
        order_obj = OrderItems.objects.get(uid = order_uid)
        order_obj.status = "Canceled"
        wallet, created = Wallet.objects.get_or_create(user=request.user.profile)
        wallet.amount += order_obj.product_price
        wallet.save()
        order_obj.save()
        product_stock = ProductVarient.objects.get(size = order_obj.size, product = order_obj.product)
        product_stock.stock += order_obj.quantity
        product_stock.sold -= order_obj.quantity
        product_stock.save()
        messages.success(request, "Order canceled successfully!")
        return redirect(f'/account/order/{request.user.profile.uid}')
    except Exception as e:
        return HttpResponse(e)
    
def address_listing(request):
    users = request.user
    context = {}
    context['addresses'] = Address.objects.filter(user = users,unlisted = False)
    return render(request, 'accounts/profile/address.html',context)

def address_adding(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        user = request.user
        street_address = request.POST.get('street_address')
        local_place = request.POST.get('local_place')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        phone_number = request.POST.get('phone_number')
        
        # Create a new Address object and save it
        address = Address(user=user, street_address=street_address, local_place=local_place, city=city, district=district, state=state, pin=pin, phone_number=phone_number)
        address.save()

        # Redirect to a success or confirmation page
        return redirect(reverse('address_listing'))  # Change the URL as needed

    return render(request, 'accounts/profile/add_address.html')

def address_editing(request, address_uid):
    context = {}
    address = Address.objects.get(uid=address_uid)

    if request.method == 'POST':
        # Update the address fields with the submitted values
        address.street_address = request.POST['street_address']
        address.local_place = request.POST['local_place']
        address.city = request.POST['city']
        address.district = request.POST['district']
        address.state = request.POST['state']
        address.pin = request.POST['pin']
        address.phone_number = request.POST['phone_number']
        address.save()  # Save the updated address

        # Redirect to a success page or wherever you want after the update
        return redirect(reverse('address_listing'))

    context['address'] = address
    return render(request, 'accounts/profile/edit_address.html', context)

def address_deleting(request, address_uid):
    try:
        address = Address.objects.get(uid=address_uid)
        address.unlisted = True
        address.save()
        return redirect(reverse('address_listing'))
    except Exception as e:
        return HttpResponse(e)
    
def return_order(request, order_uid):
    order = OrderItems.objects.get(uid = order_uid)
    order.status = "Returned"
    varient  = ProductVarient.objects.get(product = order.product, size = order.size)
    varient.stock += order.quantity
    varient.sold -= order.quantity
    wallet = Wallet.objects.get(user = request.user.profile)
    wallet.amount += order.sub_total
    order.save()
    wallet.save()
    varient.save()
    return redirect(reverse('order_listing', args=[str(request.user.profile.uid)]))


