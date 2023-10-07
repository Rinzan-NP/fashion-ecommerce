from django.urls import path
from . import views


urlpatterns = [
    path('user/<user_uid>', views.checkout, name = "checkout_page"),

    path('place_order/', views.create_order, name = "create_order" ),

    path('sucess_page/', views.success, name = "success"),

]
