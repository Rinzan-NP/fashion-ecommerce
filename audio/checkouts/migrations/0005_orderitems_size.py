# Generated by Django 4.2.5 on 2023-10-04 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_remove_cart_total_price_remove_cartitems_sub_total'),
        ('checkouts', '0004_remove_orderitems_status_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='size',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='products.size'),
            preserve_default=False,
        ),
    ]