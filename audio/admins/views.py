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
        category = request.POST.get('category')
        
        image = request.FILES.get('main_image')
        image_side = request.FILES.get('side_image')
        image_back = request.FILES.get('back_image')
        image_up = request.FILES.get('up_image')
       
        try:
            color_obj = Color.objects.get(color_name = color)
            brand_obj = Brand.objects.get(brand_name = brand)
            size_obj = Size.objects.get(size = size)
            category_obj = Category.objects.get(category_name = category)
            product_obj = Product.objects.filter(name = name,description = description,selling_price = selling_price, color = color_obj,brand = brand_obj, size =size_obj,main_image =image, category = category_obj)
        except Exception as e:
            return HttpResponse(e)
        if Product.objects.filter(name = name,description = description,selling_price = selling_price, color = color_obj,brand = brand_obj, size =size_obj,main_image =image, category = category_obj).exists():
            messages.warning(request, 'Product already exist!')
            return redirect(reverse('product_adding'))
        elif not product_obj.exists():
            # try:
            Product.objects.create(name = name, description = description, price = price, selling_price = selling_price, stock = stock,color = color_obj,brand = brand_obj,main_image = image,category = category_obj,size = size_obj)
            product_obj = Product.objects.get(name = name, description = description, price = price, selling_price = selling_price, stock = stock,color = color_obj,brand = brand_obj,category = category_obj,size = size_obj)
            Product_image.objects.create(product = product_obj, image_side = image_side, image_back = image_back, image_up = image_up)
            messages.success(request, 'Product added successfully!')
            return redirect(reverse('product_adding'))
            # except Exception as e:
            #     return HttpResponse(e)


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
        main_image = request.FILES.get('main_image') if 'main_image' in request.FILES else None
        category = request.POST.get('category')
        side_image = request.FILES.get('side_image') if 'side_image' in request.FILES else None
        back_image = request.FILES.get('back_image') if 'back_image' in request.FILES else None
        up_image = request.FILES.get('up_image') if 'up_image' in request.FILES else None

        try:
            size_instance = Size.objects.get(size=size)
            color_instance = Color.objects.get(color_name=color)
            brand_instance = Brand.objects.get(brand_name=brand)
            category_instance = Category.objects.get(category_name=category)

            products.name = name
            products.description = description
            products.size = size_instance
            if main_image is not None:
                products.main_image = main_image
            products.stock = stock
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
                return redirect(reverse('category_listing'))
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

def color_listing(request):
    context = {}
    colors = Color.objects.all()
    context['colors'] = colors
    return render(request, 'admins/color/color.html', context)

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

def brand(request):
    context = {}
    brands = Brand.objects.all()
    context['brands'] = brands
    return render(request, 'admins/brand/brand.html', context)

def brand_editing(request, id):
    context = {}
    brand = Brand.objects.get(id = id)
    if request.method == "POST":
        name = request.POST.get('name')
        if Brand.objects.filter(brand_name = name).exists():
            messages.warning(request, 'Brand already exist!')
            return redirect(reverse("brand_editing"))
        else:
            try:
                brand.brand_name = name
                brand.save()
                return redirect(reverse("brand"))
            except Exception as e:
                return HttpResponse(e)
    context['brand'] = brand
    return render(request, 'admins/brand/brand_editing.html', context)

def brand_deleting(request, id):
    brand = Brand.objects.get(id = id)
    if brand.unlisted is True:
        brand.unlisted = False
        brand.save()
    elif  brand.unlisted is False:
        brand.unlisted = True
        brand.save()
    return redirect(reverse('brand'))

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

