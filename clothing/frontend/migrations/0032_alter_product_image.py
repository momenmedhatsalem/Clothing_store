# Generated by Django 3.2.10 on 2023-06-24 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0031_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='static/images'),
        ),
    ]
