from django.urls import path
from . import views


urlpatterns = [
    path('user/<user_uid>', views.checkout, name = "checkout_page"),

    path('place_order/', views.create_order, name = "create_order" ),

    path('sucess_page/<uid>', views.success, name = "success"),

    path('verify_payment/', views.verify_payment, name = "verify_payment"),

    path('update_order_status/', views.update_status, name = "order_status"),

    path('payment_failed/', views.payment_failed, name = "payment_failed"),

    path('delete_order/', views.delete_order, name = "delete_order"),
    path('wallet/', views.wallet, name="wallet"),
    path('validate_coupon/', views.validate_coupon, name='validate_coupon'),
    path('success_page/<uid>', views.success_page, name="success_page"),
    path('success_pages/<uid>', views.success_pages, name="success_pages"),
    path('invoice/<order_uid>', views.invoice, name= "invoice")
]
