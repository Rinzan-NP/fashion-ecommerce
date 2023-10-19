from django.urls import path
from . import views


urlpatterns = [
   path('register/',views.register, name = "account"),
   path('verify/<email_token>/', views.verify_email, name = "verify_email"),
   path('login/',views.logining, name = "logining"),
   path('logouting/', views.logouting, name = 'logouting'),
   path('verify_account/',views.verify_account, name = "verify_account"),
   path('change_password/<forgot_password_token>',views.change_password, name = "check_account"),
   path('verify_email/',views.email_verification, name = "verify_email_account"),

   path('wishlist/<uid>/', views.wishlist_listing, name = "wishlisting_listing"),
   path('cart/<uid>/', views.cart_listing, name = "cart_listing"),
   
   path('profile/<uid>', views.profile, name = "profile"),
   path('order/<user_uid>', views.order_listing, name = "order_listing"),
   path('order_detail/<order_uid>', views.order_detail, name = "order_detail"),
   path('order_cancel/<order_uid>', views.order_canceling, name = "order_canceling"),
   path('return_order/<order_uid>', views.return_order, name = "return_order"),

 
   path('addresses/', views.address_listing, name = "address_listing"),
   path('add_address/', views.address_adding, name = "aderess_adding"),
   path('delete_address/<address_uid>', views.address_deleting, name = "address_deleting"),
   path('edit_address/<address_uid>', views.address_editing, name = "address_editing"),

   path("wallet/", views.wallet_history, name="wallet_history"),
]
