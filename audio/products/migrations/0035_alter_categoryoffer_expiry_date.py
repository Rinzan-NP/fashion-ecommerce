# Generated by Django 4.2.5 on 2023-10-17 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_categoryoffer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryoffer',
            name='expiry_date',
            field=models.DateField(auto_now=True),
        ),
    ]
