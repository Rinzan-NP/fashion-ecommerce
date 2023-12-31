from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.dashboard, name = "admin_dashboard"),

    path('login/',views.logining, name = "admin_login"),
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

    path('order/', views.order, name = "admin_order_listing"),
    path('order_detail/<order_uid>', views.order_detail, name = "admin_order_detail"),

    path('review/', views.review_listing, name = "admin_review_listing"),
    path('review/detail/<uid>', views.review_detail, name="review_detail"),

    path('coupon/', views.coupon_listing, name= "coupon_listing"),
    path('coupon/add', views.coupon_adding, name= "coupon_adding"),
    path('coupon/detail/<coupon_uid>', views.coupon_editing, name = "coupon_editing"),
    path('coupon/delete/<uid>', views.coupon_delete, name = "coupon_deleting"),
    
    path('banner/', views.banner, name = "banner_listing"),
    path('banner/add/', views.banner_adding, name = "banner_adding"),
    path('banner/delete/<uid>', views.banner_deleting, name = "block banner"),

    path('salesreport/', views.sales_report, name = "sales_report")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    