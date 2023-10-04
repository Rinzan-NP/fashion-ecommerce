import random
from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from products.models import Product,Cart,Profile,Size,CartItems
from datetime import timedelta
from django.db.models.signals import pre_save
from django.dispatch import receiver
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
    order_id = models.PositiveIntegerField(blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderItems")    
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_to_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new instance
            # Generate a unique 6-digit number
            while True:
                six_digit_number = random.randint(100000, 999999)
                if not Order.objects.filter(order_id=six_digit_number).exists():
                    self.order_id = six_digit_number
                    break
        super(Order, self).save(*args, **kwargs)

        
    def calculate_bill_amount(self):
        # Calculate the bill_amount as the sum of sub_total for all OrderItems
        total = sum(item.sub_total for item in self.orderitems.all())
        self.bill_amount = total
        self.amount_to_pay = total + 50
        self.save()

class OrderItems(BaseModel):
    order = models.ForeignKey(Order,related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=40, default="Pending")

@receiver(pre_save, sender=Order)
def generate_unique_six_digit_field(sender, instance, **kwargs):
    if not instance.order_id:
        # Generate a unique 6-digit number
        while True:
            six_digit_number = random.randint(100000, 999999)
            if not Order.objects.filter(order_id=six_digit_number).exists():
                instance.order_id = six_digit_number
                break