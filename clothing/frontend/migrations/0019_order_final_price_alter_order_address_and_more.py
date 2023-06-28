# Generated by Django 4.2.2 on 2023-06-21 06:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("frontend", "0018_alter_order_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="final_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="order",
            name="address",
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name="order",
            name="city",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="order",
            name="email",
            field=models.EmailField(max_length=254),
        ),
    ]
