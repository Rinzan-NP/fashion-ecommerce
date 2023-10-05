from django.urls import path
from . import views


urlpatterns = [
    path('wishlist/<user_uid>/<product_uid>', views.wishlist_management, name="wishlist_management"),

    path('cart/<product_uid>/<size_id>' , views.add_to_cart, name = "add_to_cart"),



    path('carts/delete/<uid>/', views.cart_deleting, name='cart_delete'),
    path('carts/inc/<uid>/<product_uid>', views.quantity_increasing),
    path('carts/dec/<uid>/<product_uid>', views.quantity_decreasing)
    
]
