# Generated by Django 4.2.5 on 2023-10-11 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkouts', '0018_remove_order_is_paid_orderitems_is_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='minimum_amount',
        ),
    ]