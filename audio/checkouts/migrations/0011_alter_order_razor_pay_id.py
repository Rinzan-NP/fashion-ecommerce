# Generated by Django 4.2.5 on 2023-10-07 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkouts', '0010_remove_orderitems_is_paid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='razor_pay_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
