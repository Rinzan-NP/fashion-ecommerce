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
    discount_percentage = models.IntegerField()
    maximum_use = models.IntegerField(default=1)
    minimum_amount = models.IntegerField(default = 1000)
    unlisted = models.BooleanField(default=False)

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.PositiveIntegerField(blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100, null=True,blank=True)
    local_place = models.CharField(max_length=100, null=True,blank=True)
    city = models.CharField(max_length=100, null=True,blank=True)
    district = models.CharField(max_length=100, null=True,blank=True)
    state = models.CharField(max_length=100, null=True,blank=True)
    pin = models.CharField(max_length=6, null=True,blank=True)
    phone_number = models.CharField(max_length=10, null=True,blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderItems")    
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_to_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    razor_pay_id = models.CharField(blank=True, null=True, max_length=100)
    wallet_applied = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon,on_delete= models.CASCADE, null=True, blank=True)



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
        self.save()

class OrderItems(BaseModel):
    order = models.ForeignKey(Order,related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discounted_subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=40, default="Pending")
    is_paid = models.BooleanField(default=False)


@receiver(pre_save, sender=Order)
def generate_unique_six_digit_field(sender, instance, **kwargs):
    if not instance.order_id:
        # Generate a unique 6-digit number
        while True:
            six_digit_number = random.randint(100000, 999999)
            if not Order.objects.filter(order_id=six_digit_number).exists():
                instance.order_id = six_digit_number
                break

class Wallet(BaseModel):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="wallet")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class WalletHistory(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="wallet_history")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    action = models.CharField(max_length=10)

    
class CouponHistory(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="history")

