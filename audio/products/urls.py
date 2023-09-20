from django.urls import path
from . import views


urlpatterns = [
    path('wishlist/<user_uid>/<product_uid>', views.wishlist_management, name="wishlist_management")
       
]
