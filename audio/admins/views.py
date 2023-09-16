from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from products.models import Product,Category,Size,Brand,Color,Product_image
from account.models import Profile
# Create your views here.
def dashboard(request):
    if  request.user.is_authenticated:
        return render(request, 'admins/index.html')
    else:
        return redirect(logining)

def logining(request):
    if request.user.is_authenticated:
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
    products = Product.objects.all()
    categories = Category.objects.all()
    sizes = Size.objects.all()
    brands = Brand.objects.all()
    context['categories'] = categories
    context['products'] = products
    context['brands'] = brands
    context['sizes'] = sizes
    return render(request, 'admins/products.html', context)

def product_adding(request):
    context={}

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        selling_price = request.POST.get('selling_price')
        stock = request.POST.get('stock')
        color = request.POST.get('color')
        brand = request.POST.get('brand')
        size = request.POST.get('size')
        image = request.POST.get('image')
        category = request.POST.get('category')
        image_side = request.POST.get('side_image')
        image_back = request.POST.get('back_image')
        image_up = request.POST.get('up_iamge')
        try:
            color_obj = Color.objects.get(color_name = color)
            brand_obj = Brand.objects.get(brand_name = brand)
            size_obj = Size.objects.get(size = size)
            category_obj = Category.objects.get(category_name = category)
            product_obj = Product.objects.filter(name = name,description = description,selling_price = selling_price, color = color_obj,brand = brand_obj, size =size_obj,main_image =image, category = category_obj)
        except Exception as e:
            return HttpResponse(e)
        if product_obj.exists():
            messages.warning(request, 'Product already exist!')
            return redirect(reverse('product_adding'))
        elif not product_obj.exists():
            try:
                Product.objects.create(name = name, description = description, price = price, selling_price = selling_price, stock = stock,color = color_obj,brand = brand_obj,main_image = image,category = category_obj,size = size_obj)
                product_obj = Product.objects.get(name = name, description = description, price = price, selling_price = selling_price, stock = stock,color = color_obj,brand = brand_obj,main_image = image,category = category_obj,size = size_obj)
                Product_image.objects.create(product = product_obj, image_side = image_side, image_back = image_back, image_up = image_up)
                messages.success(request, 'Product added successfully!')
                return redirect(reverse('product_adding'))
            except Exception as e:
                return HttpResponse(e)


    categories = Category.objects.all()
    sizes = Size.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    context['categories'] = categories
    context['brands'] = brands
    context['sizes'] = sizes
    context['colors'] = colors
    return render(request, 'admins/add_product.html', context)

def user_listing(request):
    context = {}
    user_obj = User.objects.all()
    profile_obj = Profile.objects.all()
    context['users'] = user_obj
    context['profiles'] = profile_obj
    return render(request, 'admins/user.html', context)

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

def staff_listing(request):
    context = {}
    
    # Filter User objects to get only those who don't have a related Profile
    users_without_profiles = User.objects.filter(profile__isnull=True)
    
    context['users'] = users_without_profiles
    
    return render(request, 'admins/staff.html', context)

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

def product_editing(request , uid):
    context = {}
    products = Product.objects.get(uid = uid)
    image = Product_image.objects.get(product = products)
    categories = Category.objects.all()
    sizes = Size.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        selling_price = request.POST.get('selling_price')
        stock = request.POST.get('stock')
        color = request.POST.get('color')
        brand = request.POST.get('brand')
        size = request.POST.get('size')
        main_image = request.POST.get('main_image')
        category = request.POST.get('category')
        image_side = request.POST.get('side_image')
        image_back = request.POST.get('back_image')
        image_up = request.POST.get('up_image')
        try:
            size_instance = Size.objects.get(size = size)
            color_instance = Color.objects.get(color_name = color)
            brand_instance = Brand.objects.get(brand_name = brand)
            category_instance = Category.objects.get(category_name = category)
            products.name = name
            products.description = description
            products.size = size_instance
            products.main_image = main_image
            products.stock = stock
            products.color = color_instance
            products.brand = brand_instance
            products.category = category_instance
            products.price = price
            products.selling_price = selling_price
            image.image_side = image_side
            image.image_back = image_back
            image.image_up = image_up
            products.save()
            image.save()
            messages.success(request, 'Edited Successfully!')
            return redirect(reverse('product_listing'))
        except Exception as e:
            return HttpResponse(e)
        
    context['categories'] = categories
    context['brands'] = brands
    context['sizes'] = sizes
    context['colors'] = colors
    context['product'] = products
    context['image'] = image

    return render(request, 'admins/product_editing.html', context)   

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
    
def category_listing(request):
    context = {}
    categories = Category.objects.all()
    context['categories'] = categories
    return render(request, 'admins/category/category.html', context)

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
    
def category_editng(request, id):
    context = {}
    category = Category.objects.get(id = id)
    if request.method == "POST":
        name = request.POST.get('name')
        if Category.objects.filter(name = name).exists():
            messages.warning(request, 'Category already exist!')
            return redirect(reverse("category_editing"))
        else:
            try:
                category.name = name
                category.save()
            except Exception as e:
                return HttpResponse(e)
    context['category'] = category
    return render(request, 'admins/category/category_editing.html', context)

def category_deleting(request, id):
    category = Category.objects.get(id = id)
    if category.unlisted is True:
        category.unlisted = False
        category.save()
    elif  category.unlisted is False:
        category.unlisted = True
        category.save()
    return redirect(reverse('category_listing'))
