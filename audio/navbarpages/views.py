from django.shortcuts import render,render
from products.models import Product,Product_image,Category,Size,Color

# Create your views here.
def home(request):
    context = {}
    latest_products = Product.objects.order_by('-created_at')[:8]
    context['products'] = latest_products
    return render(request, 'navbarpages/index.html', context)

def shop_listing(request):
    context = {}
    product_obj = Product.objects.all()
    categories = Category.objects.all()
    sizes = Size.objects.all()
    color = Color.objects.all()
    context['products'] = product_obj
    context['categories'] = categories
    context['sizes'] = sizes
    context['colors'] = color

    return render(request, 'navbarpages/shop.html', context)

def product_detail(request, uid):
    context = {}
    product_obj = Product.objects.get(uid = uid)
    product_img_obj = Product_image.objects.get(product = product_obj)
    context['products'] = product_obj
    context['images'] = product_img_obj
    return render(request, 'navbarpages/product_detail.html', context)

