# Generated by Django 4.2.5 on 2023-10-18 04:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0039_alter_categoryoffer_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryoffer',
            name='expiry_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
