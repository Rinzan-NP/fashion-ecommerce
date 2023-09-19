from django.urls import path
from . import views


urlpatterns = [
    path('wishlist/<user_id>/<product_id>', views.wishlist_management, name="wishlist_management")
       
]
