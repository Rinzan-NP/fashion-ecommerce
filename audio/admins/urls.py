from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.dashboard, name = "admin_dashboard"),
    path('login/',views.logining, name = "admin_dashboard"),
    path('logouting/', views.logouting, name='logouting'),
    path('products/', views.product_listing, name = "product_listing"),
    path('products/add_product/', views.product_adding, name = "product_adding"),
    path('users/', views.user_listing, name = "user_listing"),
    path('users/block/<uid>/', views.user_blocking, name = "user_blocking"),
    path('users/add_user',views.add_user, name = "add_user"),
    path('staffs/', views.staff_listing, name = "staff_listing"),
    path('staffs/block/<int:id>', views.staff_blocking, name = "staff_blocking"),
    path('staffs/add_staff', views.staff_adding, name = "staff_adding"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    