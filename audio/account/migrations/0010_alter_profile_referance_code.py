# Generated by Django 4.2.5 on 2023-10-13 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_profile_referance_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='referance_code',
            field=models.CharField(max_length=12),
        ),
    ]
