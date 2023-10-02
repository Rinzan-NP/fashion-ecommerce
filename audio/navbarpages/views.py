from django.shortcuts import render,render
from products.models import Product,Product_image,Category,Size,Color,Brand,Wishlist,Cart,Profile,CartItems
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    context = {}
    latest_products = Product.objects.filter(is_selling = True,
        category__unlisted=False,
        
        brand__unlisted=False).order_by('-created_at')[:8]
    context['products'] = latest_products

    if request.user.is_authenticated and request.user.is_staff is False:
        context['wishlist'] = [item.product for item in Wishlist.objects.filter(user=request.user.profile)]
        user_cart_items = CartItems.objects.filter(cart__user=request.user.profile)
        context['cart'] = [item.product for item in user_cart_items]
    return render(request, 'navbarpages/index.html', context)


def shop_listing(request):
    context = {}
    
    # Filter products that are not unlisted in Category, Size, and Brand
    product_obj = Product.objects.filter(
        is_selling=True,
        category__unlisted=False,
        brand__unlisted=False
    )
    

    categories = Category.objects.filter(unlisted=False)
    brands = Brand.objects.filter(unlisted=False)
    sizes = Size.objects.all()
    colors = Color.objects.all()

    # Initialize Paginator
    paginator = Paginator(product_obj, 9)  # 12 products per page

    page = request.GET.get('page')  # Get the current page number from the request's GET parameters
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results
        products = paginator.page(paginator.num_pages)

    context['products'] = products
    context['categories'] = categories
    context['sizes'] = sizes
    context['colors'] = colors
    context['brands'] = brands

    if request.user.is_authenticated and not request.user.is_staff:
        context['wishlist'] = [item.product for item in Wishlist.objects.filter(user=request.user.profile)]
        user_cart_items = CartItems.objects.filter(cart__user=request.user.profile)
        context['cart'] = [item.product for item in user_cart_items]
        context['user'] = Profile.objects.get(user = request.user)

    return render(request, 'navbarpages/shop.html', context)


def product_detail(request, uid):
    context = {}
    product_obj = Product.objects.get(uid = uid)
    product_img_obj = Product_image.objects.get(product = product_obj)
    category_obj = product_obj.category
    products_with_category = Product.objects.filter(category = category_obj)
    if request.user.is_authenticated and request.user.is_staff is False:
        context['wishlist'] = [item.product for item in Wishlist.objects.filter(user=request.user.profile)]
        user_cart_items = CartItems.objects.filter(cart__user=request.user.profile)
        context['cart'] = [item.product for item in user_cart_items]
        context['user'] = Profile.objects.get(user = request.user)
    context['products'] = product_obj
    context['images'] = product_img_obj
    context['category_products'] = products_with_category
    return render(request, 'navbarpages/product_detail.html', context)

