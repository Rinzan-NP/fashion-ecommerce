# Generated by Django 4.2.5 on 2023-10-10 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkouts', '0014_alter_wallet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='wallet_applied',
            field=models.BooleanField(default=False),
        ),
    ]
