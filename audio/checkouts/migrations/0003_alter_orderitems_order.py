# Generated by Django 4.2.5 on 2023-09-30 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkouts', '0002_remove_order_coupon_remove_order_delivery_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='checkouts.order'),
        ),
    ]
