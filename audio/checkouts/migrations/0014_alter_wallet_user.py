# Generated by Django 4.2.5 on 2023-10-09 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_profile_profile_image'),
        ('checkouts', '0013_alter_wallet_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to='account.profile'),
        ),
    ]