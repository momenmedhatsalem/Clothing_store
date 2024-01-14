# Generated by Django 4.2.2 on 2023-06-20 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("frontend", "0012_cart_shipping_cost"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="myuser",
            name="address",
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("country", models.CharField(default="Egypt", max_length=100)),
                ("address", models.CharField(max_length=100)),
                ("street_name", models.CharField(max_length=200)),
                ("building", models.CharField(max_length=200)),
                ("city", models.CharField(max_length=100)),
                ("governorate", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=100)),
                ("Nearest_landmark", models.CharField(max_length=100)),
                ("is_default", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]