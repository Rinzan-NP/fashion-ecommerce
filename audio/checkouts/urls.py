from django.urls import path
from . import views


urlpatterns = [
    path('user/<user_uid>', views.checkout, name = "checkout_page"),
    path('order_placed/', views.order_placed, name = "order_placed"),
    path('check_cart/', views.check_cart , name = "checking_cart")
]
