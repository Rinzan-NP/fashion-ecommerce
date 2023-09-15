from django.db import models
from base.models import BaseModel
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    unlisted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.category_name


class Size(models.Model):
    size = models.IntegerField()
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        str_size = str(self.size)
        return str_size


class Brand(models.Model):
    brand_name = models.CharField(max_length=50)
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return self.brand_name
    

class Color(models.Model):
    color_name = models.CharField(max_length=100)
    hexcode = models.CharField(max_length=50)

    def __str__(self):
        return self.color_name
    

class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    main_image = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    selling_price = models.DecimalField(max_digits=7, decimal_places=2)
    brand = models.ForeignKey(Brand, related_name='brand_of_product', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category_of_product', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name='size_of_product', on_delete=models.CASCADE)
    stock = models.IntegerField()
    is_selling = models.BooleanField(default=True)
    color = models.ForeignKey(Color, related_name='color_of_product', on_delete=models.CASCADE)
    unlisted = models.BooleanField(default=False)


    def __str__(self):
        return self.name
    

class Product_image(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    image_side = models.CharField(max_length=255, null=True, blank=True)
    image_back = models.CharField(max_length=255, null=True, blank=True)
    image_up = models.CharField(max_length=255, null=True, blank=True)

    

    def __str__(self):
        return self.product.name
    
