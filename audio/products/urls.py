from django.urls import path
from . import views


urlpatterns = [
    path('wishlist/<user_uid>/<product_uid>', views.wishlist_management, name="wishlist_management"),
    path('cart/<user_uid>/<product_uid>', views.cart_management, name="cart_management"),
    
    path('carts/delete/<uid>/', views.cart_deleting, name='cart_delete'),
    path('carts/inc/<uid>', views.quantity_increasing),
    path('carts/dec/<uid>', views.quantity_decreasing)
    
]
