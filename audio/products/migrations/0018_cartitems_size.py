# Generated by Django 4.2.5 on 2023-10-02 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_remove_size_unlisted'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='size',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='products.size'),
        ),
    ]