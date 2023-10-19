from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from products.models import Banner, CategoryOffer, Product,Category, Review,Size,Brand,Color,Product_image,ProductVarient
from account.models import Profile
from checkouts.models import Coupon, Order,OrderItems, Wallet, WalletHistory
from .decarator import admin_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Q
# Create your views here.
def dashboard(request):
    if  request.user.is_authenticated and request.user.is_staff is True:
        context = {}
        try:
            new_user = Profile.objects.filter(email_verified = True).order_by('created_at')[3]
        except:
            new_user = Profile.objects.filter(email_verified = True).order_by('created_at')
        now = timezone.now()
        start_month = timezone.datetime(now.year, now.month, 1) 
        delivered_products = OrderItems.objects.filter(status='Delivered', created_at__gte=start_month)
        monthly_revenue = delivered_products.aggregate(revenue=Sum('discounted_subtotal'))['revenue']
        orders = Order.objects.all()
        context['orders'] = orders
        no_of_cod = Order.objects.filter(payment_method__method = "COD").count()
        no_of_upi = Order.objects.filter(payment_method__method = "Razor_pay").count()
        try:
            upi_percent = round((no_of_upi/(no_of_upi + no_of_cod)) * 100, 2)
            cod_percent = round((no_of_cod/(no_of_cod + no_of_upi)) * 100, 2)
        except: 
            cod_percent = 100
            upi_percent = 100

        now = datetime.now()
        year = now.year
        month = now.month
        monthly_order_counts = []
        monthly_product_count = []
        monthly_user_count = []
        for m in range(1, month + 1):
            start_date = datetime(year, m, 1)
            if m == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, m + 1, 1)

           
            orders_count = Order.objects.filter(
                created_at__range=(start_date, end_date)
            ).aggregate(order_count=Count('uid'))['order_count']
            monthly_order_counts.append(orders_count or 0)
            
            products_count = Product.objects.filter(
                created_at__range=(start_date, end_date)
            ).aggregate(product_count=Count('uid'))['product_count']
            monthly_product_count.append(products_count or 0)

            users_count = Profile.objects.filter(
                created_at__range=(start_date, end_date)
            ).aggregate(user_count=Count('uid'))['user_count']
            monthly_user_count.append(users_count or 0)




        delivered_items = OrderItems.objects.filter(status="Delivered")
        total = delivered_items.aggregate(total_discounted_subtotal=Sum('discounted_subtotal'))['total_discounted_subtotal']
        context['no_of_product'] = Product.objects.filter(is_selling = True).count()
        context['delivered'] = OrderItems.objects.filter(status = "Delivered").count()
        context['orders'] = Order.objects.all().order_by('-created_at')[:6]
        context['monthly_revenue'] = monthly_revenue
        context['new_user'] = new_user
        context['revenue'] = total
        context['cod'] = cod_percent
        context['upi'] = upi_percent
        context['sales'] = monthly_order_counts
        context['products'] = monthly_product_count
        context['users'] = monthly_user_count

        return render(request, 'admins/index.html',context)
    else:
        return redirect(logining)

def logining(request):
    if request.user.is_authenticated and request.user.is_staff is True:
        return redirect('/admin/')  # Redirect if the user is already authenticated

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username and password exists
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)  # Log in the user
                return redirect('/admin/')
            else:
                messages.warning(request, 'You do not have staff privileges.')
        else:
            messages.warning(request, 'Invalid credentials.')

    return render(request, 'admins/login.html')
    
def logouting(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/') 
    
def product_listing(request):
    context = {}
    if  request.user.is_authenticated and request.user.is_staff is True:
        products = Product.objects.all()
        categories = Category.objects.all()
        sizes = Size.objects.all()
        brands = Brand.objects.all()
        context['categories'] = categories
        context['products'] = products
        context['brands'] = brands
        context['sizes'] = sizes
        return render(request, 'admins/products.html', context)
    else:
        return redirect(logining)

def product_adding(request):
    context={}

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        selling_price = request.POST.get('selling_price')
        stock_8 = request.POST.get('stock8')
        stock_9 = request.POST.get('stock9')
        stock_10  = request.POST.get('stock10')
        color = request.POST.get('color')
        brand = request.POST.get('brand')
       
        category = request.POST.get('category')
        
        image = request.FILES.get('main_image')
        image_side = request.FILES.get('side_image')
        image_back = request.FILES.get('back_image')
        image_up = request.FILES.get('up_image')
       
        try:
            color_obj = Color.objects.get(color_name = color)
            brand_obj = Brand.objects.get(brand_name = brand)
            size_obj_8 = Size.objects.get(size = 8)
            size_obj_9 = Size.objects.get(size = 9)
            size_obj_10 = Size.objects.get(size = 10)
            category_obj = Category.objects.get(category_name = category)
            product_obj = Product.objects.filter(name = name,description = description,selling_price = selling_price, color = color_obj,brand = brand_obj,main_image =image, category = category_obj)
        except Exception as e:
            return HttpResponse(e)
        if Product.objects.filter(name = name,description = description,selling_price = selling_price, color = color_obj,brand = brand_obj,main_image =image, category = category_obj).exists():
            messages.warning(request, 'Product already exist!')
            return redirect(reverse('product_adding'))
        elif not product_obj.exists():
            # try:
            Product.objects.create(name = name, description = description, price = price, selling_price = selling_price,color = color_obj,brand = brand_obj,main_image = image,category = category_obj)
            product_obj = Product.objects.get(name = name, description = description, price = price, selling_price = selling_price,color = color_obj,brand = brand_obj,category = category_obj)
            Product_image.objects.create(product = product_obj, image_side = image_side, image_back = image_back, image_up = image_up)
            ProductVarient.objects.create(product = product_obj,size = size_obj_8, stock = stock_8)
            ProductVarient.objects.create(product = product_obj,size = size_obj_9, stock = stock_9)
            ProductVarient.objects.create(product = product_obj,size = size_obj_10, stock = stock_10)
            messages.success(request, 'Product added successfully!')
            return redirect(reverse('product_adding'))
           

    if  request.user.is_authenticated and request.user.is_staff is True:
        categories = Category.objects.all()
        sizes = Size.objects.all()
        brands = Brand.objects.all()
        colors = Color.objects.all()
        context['categories'] = categories
        context['brands'] = brands
        context['sizes'] = sizes
        context['colors'] = colors
        return render(request, 'admins/add_product.html', context)
    else:
        return redirect(logining)

def user_listing(request):
    context = {}
    if  request.user.is_authenticated and request.user.is_staff is True:
        user_obj = User.objects.all()
        profile_obj = Profile.objects.all()
        context['users'] = user_obj
        context['profiles'] = profile_obj
        return render(request, 'admins/user.html', context)
    else:
        return redirect(logining)

@admin_required
def user_blocking(request, uid):
    try:
        profile_obj = Profile.objects.get(uid = uid)
        if profile_obj.is_blocked :
            profile_obj.is_blocked  = False
            profile_obj.save()
        elif profile_obj.is_blocked is False:
            profile_obj.is_blocked = True
            profile_obj.save()
        return redirect(user_listing)
    except Exception as e:
        return HttpResponse(e)

@admin_required
def add_user(request):
    if request.method == "POST":
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        re_password = request.POST.get('pass2')
        if password == re_password and len(password) < 8:
            messages.warning(request, "Passwords must be minimum of 8 length.")  
        elif password == re_password and len(password)  > 8:
            if User.objects.filter(username=email).exists():
                messages.warning(request, "Email already taken!")
                return HttpResponseRedirect(request.path_info)
            else:
                user = User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name)
                messages.success(request, "An email is sent to your email to verify your email.")
                return HttpResponseRedirect(request.path_info)
   
        else:
            messages.warning(request, "Passwords do not match .")
            return HttpResponseRedirect(request.path_info)


    return render(request, 'admins/user_register.html')

@admin_required
def staff_listing(request):
    context = {}
    
    # Filter User objects to get only those who don't have a related Profile
    users_without_profiles = User.objects.filter(profile__isnull=True)
    
    context['users'] = users_without_profiles
    
    return render(request, 'admins/staff.html', context)

@admin_required
def staff_blocking(request, id):
    try:
        user_obj = User.objects.get(id = id)
        if user_obj.is_staff is True:
            user_obj.is_staff  = False
            user_obj.save()
        elif user_obj.is_staff is False:
            user_obj.is_staff = True
            user_obj.save()
        return redirect(staff_listing)
    except Exception as e:
        return HttpResponse(e)
    
@admin_required
def staff_adding(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        re_password = request.POST.get('pass2')
        if password == re_password and len(password) < 8:
            messages.warning(request, "Passwords must be minimum of 8 length.")  
        elif password == re_password and len(password)  > 8:
            if User.objects.filter(username=username).exists():
                messages.warning(request, "username already taken!")
                return HttpResponseRedirect(request.path_info)
            else:
                user = User.objects.create_user(username=username, password=password,is_staff = True)
                messages.success(request, "Staff created successfully")
                return HttpResponseRedirect(request.path_info)
   
        else:
            messages.warning(request, "Passwords do not match .")
            return HttpResponseRedirect(request.path_info)


    return render(request, 'admins/staff_register.html')

@admin_required
def product_editing(request , uid): 
    context = {}
    products = Product.objects.get(uid = uid)
    image = Product_image.objects.get(product = products)
    categories = Category.objects.all()
    sizes = Size.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    size_obj_8 = Size.objects.get(size = 8)
    size_obj_9 = Size.objects.get(size = 9)
    size_obj_10 = Size.objects.get(size = 10)

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        selling_price = request.POST.get('selling_price')
        color = request.POST.get('color')
        brand = request.POST.get('brand')
        stock8 =request.POST.get('stock8')
        stock9 =request.POST.get('stock9')
        stock10 =request.POST.get('stock10')
        main_image = request.FILES.get('main_image') if 'main_image' in request.FILES else None
        category = request.POST.get('category')
        side_image = request.FILES.get('side_image') if 'side_image' in request.FILES else None
        back_image = request.FILES.get('back_image') if 'back_image' in request.FILES else None
        up_image = request.FILES.get('up_image') if 'up_image' in request.FILES else None

        try:
            
            sizess = [size_obj_8,size_obj_9,size_obj_10]
            quantity_of_8 =  ProductVarient.objects.get(product = products, size = size_obj_8)  
            quantity_of_9 = ProductVarient.objects.get(product = products, size = size_obj_9)
            quantity_of_10 = ProductVarient.objects.get(product = products, size = size_obj_10)
            quantity_of_8.stock = stock8
            quantity_of_9.stock = stock9
            quantity_of_10.stock = stock10
            quantity_of_10.save()
            quantity_of_8.save()
            quantity_of_9.save()  
            color_instance = Color.objects.get(color_name=color)
            brand_instance = Brand.objects.get(brand_name=brand)
            category_instance = Category.objects.get(category_name=category)
            
                
            
            products.name = name
            products.description = description
            
            if main_image is not None:
                products.main_image = main_image
            
            products.color = color_instance
            products.brand = brand_instance
            products.category = category_instance
            products.price = price
            products.selling_price = selling_price

            if side_image is not None:
                image.image_side = side_image
            if back_image is not None:
                image.image_back = back_image
            if up_image is not None:
                image.image_up = up_image

            products.save()
            if main_image is not None:
                products.main_image.save(main_image.name, main_image)

            image.save()
            if side_image is not None:
                image.image_side.save(side_image.name, side_image)
            if back_image is not None:
                image.image_back.save(back_image.name, back_image)
            if up_image is not None:
                image.image_up.save(up_image.name, up_image)

            messages.success(request, 'Edited Successfully!')
            return redirect(reverse('product_listing'))
            
        except Exception as e:
            return HttpResponse(e)
   
    context['categories'] = categories
    context['brands'] = brands
    context['sizes'] = sizes
    context['stock_8'] = ProductVarient.objects.get(product = products, size = size_obj_8).stock
    context['stock_9'] = ProductVarient.objects.get(product = products, size = size_obj_9).stock
    context['stock_10'] = ProductVarient.objects.get(product = products, size = size_obj_10).stock
    context['colors'] = colors
    context['product'] = products
    context['image'] = image

    return render(request, 'admins/product_editing.html', context)

@admin_required
def product_unlisting(request, uid):
    try:
        product = Product.objects.get(uid = uid)
        if product.is_selling is True:
            product.is_selling = False
            product.save()
        elif product.is_selling is False:
            product.is_selling = True
            product.save()
        return redirect(reverse('product_listing'))
    except Exception as e:
        return HttpResponse(e)
    
@admin_required   
def category_listing(request):
    context = {}
    categories = Category.objects.all()
    context['categories'] = categories
    return render(request, 'admins/category/category.html', context)

@admin_required
def category_adding(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if Category.objects.filter(category_name = name).exists():
            messages.warning(request, "Category already exist!")
            return redirect(reverse('category_adding'))
        else:
            try:
                Category.objects.create(category_name = name)
                messages.success(request, "Category created successfylly!")
                return redirect(reverse('category_listing'))
            except Exception as  e:
                return HttpResponse(e)
    return render(request, 'admins/category/category_adding.html')

@admin_required   
def category_editng(request, id):
    context = {}
    category = Category.objects.get(id = id)
    if request.method == "POST":
        name = request.POST.get('name')   
        offer = request.POST.get('offer')
        expiry_date = request.POST.get('expiry_date')
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
        try:
            category.category_name = name
            category.save()
            category_offer, created = CategoryOffer.objects.get_or_create(category = category)
            category_offer.percentage = offer
            category_offer.expiry_date = expiry_date
            category_offer.save()
            products = Product.objects.filter(category = category)
            for product in  products:
                product.selling_price = (float(product.price) - (float(product.price) * float(category_offer.percentage)/100))
                product.save()            
            return redirect(reverse('category_listing'))
        except Exception as e:
            return HttpResponse(e)
    context['category'] = category
    return render(request, 'admins/category/category_editing.html', context)

@admin_required
def category_deleting(request, id):
    category = Category.objects.get(id = id)
    if category.unlisted is True:
        category.unlisted = False
        category.save()
    elif  category.unlisted is False:
        category.unlisted = True
        category.save()
    return redirect(reverse('category_listing'))

@admin_required
def color_listing(request):
    context = {}
    colors = Color.objects.all()
    context['colors'] = colors
    return render(request, 'admins/color/color.html', context)

@admin_required
def color_adding(request):
    if request.method == "POST":
        name = request.POST.get('name')
        hexcode = request.POST.get('hexcode')
        if Color.objects.filter(color_name = name).exists() or Color.objects.filter(hexcode = hexcode):
            messages.warning(request, 'Color already exists!')
            return redirect(reverse('color_adding'))
        else:
            try:
                Color.objects.create(color_name = name, hexcode = hexcode)
                messages.success(request, 'Color added sucessfully!')
                return redirect(reverse('color_listing'))
            except Exception as e:
                return HttpResponse(e)
    return render(request, 'admins/color/add_color.html')

@admin_required
def color_editing(request, id):
    context = {}
    color = Color.objects.get(id = id)
    context['color'] = color
    if request.method == "POST":
        name = request.POST.get('name')
        hexcode = request.POST.get('hexcode')
        try:
            color.color_name = name
            color.hexcode = hexcode
            color.save()
            messages.success(request, 'Edited Successfully!')
            return redirect(reverse('color_listing'))
        except Exception as e:
            return HttpResponse(e)

    return render(request, 'admins/color/edit_color.html', context)

@admin_required
def brand(request):
    context = {}
    brands = Brand.objects.all()
    context['brands'] = brands
    return render(request, 'admins/brand/brand.html', context)

@admin_required
def brand_editing(request, id):
    context = {}
    brand = Brand.objects.get(id = id)
    if request.method == "POST":
        name = request.POST.get('name')
        try:
            brand.brand_name = name
            brand.save()
            return redirect('/admin/brand')
        except Exception as e:
            return HttpResponse(e)
    context['brand'] = brand
    return render(request, 'admins/brand/brand_editing.html', context)

@admin_required
def brand_deleting(request, id):
    brand = Brand.objects.get(id = id)
    if brand.unlisted is True:
        brand.unlisted = False
        brand.save()
    elif  brand.unlisted is False:
        brand.unlisted = True
        brand.save()
    return redirect(reverse('brand'))

@admin_required
def brand_adding(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if Brand.objects.filter(brand_name = name).exists():
            messages.warning(request, "brand already exist!")
            return redirect(reverse('brand_adding'))
        else:
            try:
                Brand.objects.create(brand_name = name)
                messages.success(request, "Brand created successfylly!")
                return redirect(reverse('brand'))
            except Exception as  e:
                return HttpResponse(e)
    return render(request, 'admins/brand/brand_add.html')

@admin_required
def order(request):
    context = {}
    orders = Order.objects.all().order_by('-created_at')
    
    if request.method == "POST":
        order_uid = request.POST.get('uid')
        if order_uid:
            orders = Order.objects.filter(order_id__contains =order_uid).order_by('-created_at')
    
    context['orders'] = orders
    return render(request, 'admins/order/order.html', context)

@admin_required
def order_detail(request, order_uid):
    context = {}
    order = Order.objects.get(uid=order_uid)
    orders = OrderItems.objects.filter(order=order)
    context['orders'] = orders
    context['order'] = order

    if request.method == "POST":
        for item in orders:
            status = request.POST.get(f'status-{item.uid}')
            item.status = status
            item.save()
            if item.status == "Canceled" or item.status == "Returned":
                amount = item.discounted_subtotal if item.status == "Canceled" else float(item.discounted_subtotal) + 50
                wallet = Wallet.objects.get_or_create(user = order.user.profile)
                wallet[0].amount += amount
                wallet[0].save()
                WalletHistory.objects.create(wallet = wallet[0], amount = amount,action="Credit")

        return redirect(reverse('admin_order_listing'))

    return render(request, 'admins/order/order_detail.html', context)

@admin_required
def review_listing(request):
    context = {}
    reviews = Review.objects.all()

    paginator = Paginator(reviews, 10)

    
    page = request.GET.get('page')

    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reviews = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        reviews = paginator.page(paginator.num_pages)

    context['reviews'] = reviews
    return render(request, 'admins/review/review.html', context)

@admin_required
def review_detail(request, uid):
    context = {}
    review = Review.objects.get(uid = uid)
    context['review'] = review
    return render(request, 'admins/review/review_detail.html',context)

@admin_required
def coupon_listing(request):
    context = {}
    coupon = Coupon.objects.all()
    context['coupons'] = coupon
    return render(request, 'admins/coupon/coupon.html',context)

@admin_required
def coupon_adding(request):
    if request.method == "POST":
        code = request.POST['code']
        discount_percentage = request.POST['discount_percentage']
        expiry_date = request.POST['expiry_date']
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M')
        if Coupon.objects.filter(code = code).exists():
            messages.warning(request, "Coupon Already exists!")
            return redirect(reverse('coupon_adding'))
        coupon = Coupon(code=code, discount_percentage=discount_percentage, expiry_date=expiry_date)
        coupon.save()
        messages.success(request, "Coupon added successfully")
        return redirect(reverse('coupon_adding'))
    return render(request, "admins/coupon/add_coupon.html")

@admin_required
def coupon_editing(request, coupon_uid):
    coupon = Coupon.objects.get(uid = coupon_uid)
    context = {}
    if request.method =="POST":
        
        discount_percentage = request.POST['discount_percentage']
        expiry_date = request.POST['expiry_date']
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M')
        
   
        coupon.expiry_date = expiry_date
        coupon.discount_percentage = discount_percentage
        coupon.save()
        messages.success(request,"Edited successfully!")
        return redirect(reverse("coupon_listing"))
    context['coupon'] = coupon
    return render(request, 'admins/coupon/coupon_editing.html', context)
    
@admin_required
def banner(request):
    context = {}
    banners = Banner.objects.all()
    context['banners'] = banners
    return render(request, 'admins/banner/banner.html', context)

@admin_required
def banner_adding(request):
    context = {}
    if request.method == "POST":
        text = request.POST.get('banner_text')
        image = request.FILES.get('image')
        expiry_date = request.POST['expiry_date']
        product_uid = request.POST['product']

        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M')
        product = Product.objects.get(uid = product_uid)

        banner = Banner.objects.create(banner_image = image, banner_text = text, expiry_date = expiry_date, product = product)
        messages.success(request, "Banner created successfully")



    context['products'] = Product.objects.filter(is_selling = True)
    return render(request, 'admins/banner/banner_adding.html', context)

@admin_required
def banner_deleting(request, uid):
    banner = Banner.objects.get(uid = uid)
    if banner.status is True:
        banner.status = False
    else:
        banner.status = True
    banner.save()
    return redirect(reverse('banner_listing'))

@admin_required
def coupon_delete(request, uid):
    coupon = Coupon.objects.get(uid = uid)
    coupon.unlisted = True if coupon.unlisted is False else False
    coupon.save()
    return redirect(reverse('coupon_listing'))
