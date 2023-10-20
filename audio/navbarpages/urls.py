
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home , name = "index"),
    path('shop/',views.shop_listing, name = "shop_listing"),
    path('product/detail/<uid>', views.product_detail, name= "product_detail"),
    path('contact/', views.contact, name = "contact"),
    path('aboutus/',views.aboutus),
    path('404error/', views.error, name="404")
    
]
