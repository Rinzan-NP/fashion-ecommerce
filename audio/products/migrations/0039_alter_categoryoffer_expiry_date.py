# Generated by Django 4.2.5 on 2023-10-18 04:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0038_alter_product_selling_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryoffer',
            name='expiry_date',
            field=models.DateField(default=datetime.date(2023, 10, 18)),
        ),
    ]
