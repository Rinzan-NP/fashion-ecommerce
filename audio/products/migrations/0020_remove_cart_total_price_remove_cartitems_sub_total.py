# Generated by Django 4.2.5 on 2023-10-04 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_alter_cartitems_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='sub_total',
        ),
    ]