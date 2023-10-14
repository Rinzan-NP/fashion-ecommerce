from django.db import models
from django.http import HttpResponse
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from account.models import Profile
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    offer = models.IntegerField(default = 0)
    unlisted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.category_name


class Size(models.Model):
    size = models.IntegerField()
    

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
    main_image = models.ImageField(upload_to='product_images')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    selling_price = models.DecimalField(max_digits=7, decimal_places=2)
    brand = models.ForeignKey(Brand, related_name='brand_of_product', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category_of_product', on_delete=models.CASCADE)
    is_selling = models.BooleanField(default=True)
    color = models.ForeignKey(Color, related_name='color_of_product', on_delete=models.CASCADE)



    def __str__(self):
        return self.name
class ProductVarient(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    sold = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} : {self.Size}"

class Product_image(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    image_side = models.ImageField(upload_to='product_images')
    image_back = models.ImageField(upload_to='product_images')
    image_up = models.ImageField(upload_to='product_images')

    

    def __str__(self):
        return self.product.name


@receiver(post_save, sender=Product_image)
def resize_images(sender, instance, **kwargs):
    # Open the image file
    main_img = Image.open(instance.product.main_image.path)
    side_img = Image.open(instance.image_side.path)
    back_img = Image.open(instance.image_back.path)
    up_img = Image.open(instance.image_up.path)

    # Resize the images
    main_img = main_img.resize((840, 840), Image.LANCZOS)
    side_img = side_img.resize((840, 840), Image.LANCZOS)
    back_img = back_img.resize((840, 840), Image.LANCZOS)
    up_img = up_img.resize((840, 840), Image.LANCZOS)

    # Save the images
    main_img.save(instance.product.main_image.path)
    side_img.save(instance.image_side.path)
    back_img.save(instance.image_back.path)
    up_img.save(instance.image_up.path)

class Wishlist(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self) -> str:
        return f'{self.user.user.username} : {self.product.name}'

class Cart(BaseModel):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartItems")
    
    

    def __str__(self) -> str:
        return f'{self.user.user.username} : Cart'


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Cart'
    
    @property
    def is_out_of_stock(self):
        return self.quantity > ProductVarient.objects.get(product=self.product, size=self.size).stock

    def calculate_sub_total(self):
        return self.product.selling_price * self.quantity

class Review(BaseModel):
    user = models.ForeignKey(Profile,related_name="review", on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name = "product_review", on_delete=models.CASCADE)
    review = models.TextField()

    class Meta:
        unique_together = ('user', 'product')

class Banner(BaseModel):
    banncer_image = models.ImageField()
    banner_text = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    expiry_date = models.DateField(auto_now=False, auto_now_add=False)
    