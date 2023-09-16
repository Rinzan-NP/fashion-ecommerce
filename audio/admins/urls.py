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
    path('product/edit/<uid>', views.product_editing, name = "product_editing"),
    path('product/delete/<uid>', views.product_unlisting ,name = "product_unlisting"),

    path('users/', views.user_listing, name = "user_listing"),
    path('users/block/<uid>/', views.user_blocking, name = "user_blocking"),
    path('users/add_user',views.add_user, name = "add_user"),

    path('staffs/', views.staff_listing, name = "staff_listing"),
    path('staffs/block/<int:id>', views.staff_blocking, name = "staff_blocking"),
    path('staffs/add_staff', views.staff_adding, name = "staff_adding"),

    path('category/add', views.category_adding, name="category_adding"),
    path('category/', views.category_listing, name = "category_listing"),
    path('category/edit/<int:id>', views.category_editng, name = 'category_editing'),
    path('category/delete/<int:id>', views.category_deleting, name = "category_deleting"),

    path('color/', views.color_listing, name='color_listing'),
    path('color/add', views.color_adding, name='color_adding'),
    path('color/edit/<int:id>', views.color_editing, name='color_editing'),

    path('brand/', views.brand, name = "brand"),
    path('brand/edit/<int:id>', views.brand_editing, name='brand_editing'),
    path('brand/delete/<int:id>', views.brand_deleting, name = "brand_deleting"),
    path('brand/add', views.brand_adding, name="brand_adding"),






]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    