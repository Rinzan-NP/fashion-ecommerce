from django.shortcuts import redirect, render,render
from products.models import Product,Product_image,Category,Size,Color,Brand,Wishlist,Cart,Profile,CartItems
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import QueryDict

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
    query = request.GET.get('q')
    brand_filter = request.GET.get('brand')
    category_filter = request.GET.get('category')
    sort_option = request.GET.get('sort')

    # Create a QueryDict to store filter criteria for pagination links
    filter_params = QueryDict(mutable=True)

    product_obj = Product.objects.filter(
        is_selling=True,
        category__unlisted=False,
        brand__unlisted=False
    )

    categories = Category.objects.filter(unlisted=False)
    brands = Brand.objects.filter(unlisted=False)
    sizes = Size.objects.all()
    colors = Color.objects.all()

    # Apply filters to the QuerySet and add them to the filter_params
    if category_filter:
        product_obj = product_obj.filter(category=category_filter)
        filter_params['category'] = category_filter

    if query:
        product_obj = product_obj.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        filter_params['q'] = query

    if brand_filter:
        product_obj = product_obj.filter(brand=brand_filter)
        filter_params['brand'] = brand_filter

    if sort_option == 'low_to_high':
        product_obj = product_obj.order_by('price')
        filter_params['sort'] = 'low_to_high'
    elif sort_option == 'high_to_low':
        product_obj = product_obj.order_by('-price')
        filter_params['sort'] = 'high_to_low'

    paginator = Paginator(product_obj, 1)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context['products'] = products
    context['categories'] = categories
    context['sizes'] = sizes
    context['colors'] = colors
    context['brands'] = brands

    # Pass the filter_params to the template
    context['filter_params'] = filter_params.urlencode()

    if request.user.is_authenticated and not request.user.is_staff:
        context['wishlist'] = [item.product for item in Wishlist.objects.filter(user=request.user.profile)]
        context['user'] = Profile.objects.get(user=request.user)

    return render(request, 'navbarpages/shop.html', context)



def product_detail(request, uid):
    context = {}
    product_obj = Product.objects.get(uid = uid)
    product_img_obj = Product_image.objects.get(product = product_obj)
    category_obj = product_obj.category
    sizes = Size.objects.all()
    products_with_category = Product.objects.filter(category = category_obj)

    if request.method == "POST":
        size = request.POST.get('size')
        size_obj  = Size.objects.get(id = size)
        return redirect(f'/product/cart/{product_obj.uid}/{size_obj.id}')

    if request.user.is_authenticated and request.user.is_staff is False:
        context['wishlist'] = [item.product for item in Wishlist.objects.filter(user=request.user.profile)]
        user_cart_items = CartItems.objects.filter(cart__user=request.user.profile)
        context['cart'] = [item.product for item in user_cart_items]
        context['user'] = Profile.objects.get(user = request.user)
    context['products'] = product_obj
    context['sizes'] = sizes
    context['images'] = product_img_obj
    context['category_products'] = products_with_category
    return render(request, 'navbarpages/product_detail.html', context)

