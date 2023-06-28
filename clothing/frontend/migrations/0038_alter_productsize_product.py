# Generated by Django 3.2.10 on 2023-06-25 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0037_productsize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsize',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='psize', to='frontend.product'),
        ),
    ]