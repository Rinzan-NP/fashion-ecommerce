# Generated by Django 4.2.5 on 2023-10-17 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_alter_banner_banncer_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banner',
            old_name='banncer_image',
            new_name='banner_image',
        ),
    ]