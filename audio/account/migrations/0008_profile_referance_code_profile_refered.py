# Generated by Django 4.2.5 on 2023-10-13 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='referance_code',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='refered',
            field=models.CharField(blank=True, default='', max_length=12, null=True),
        ),
    ]
