from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(Product_image)
admin.site.register(Color)
admin.site.register(Wishlist)

