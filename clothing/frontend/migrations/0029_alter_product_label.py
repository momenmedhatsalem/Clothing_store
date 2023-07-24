# Generated by Django 4.2.2 on 2023-06-22 07:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("frontend", "0028_product_label_alter_product_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="label",
            field=models.CharField(
                choices=[("NEW", "primary"), ("BEST Seller", "secondary"), ("N", "")],
                default="",
                max_length=11,
            ),
        ),
    ]
