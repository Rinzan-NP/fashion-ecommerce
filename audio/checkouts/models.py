from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from products.models import Product,Cart,Profile
from datetime import timedelta
# Create your models here.
 
class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    local_place = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=10)
    unlisted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.first_name} : {self.pin}"

class PaymentMethod(BaseModel):
    method = models.CharField( max_length=50)
    
    def __str__(self) -> str:
        return self.method

class Coupon(BaseModel):
    code = models.CharField(max_length=10)
    expiry_date = models.DateTimeField()
    minimum_amount = models.IntegerField()
    discount_amount = models.IntegerField()


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    price = models.IntegerField()
    amount_to_pay = models.IntegerField()
    delivery_date = models.DateTimeField(blank=True, null=True)  # Allow for nullable delivery_date
    
    def save(self, *args, **kwargs):
        if not self.delivery_date and self.created_at:
            self.delivery_date = self.created_at + timedelta(days=5)
        super(Order, self).save(*args, **kwargs)
