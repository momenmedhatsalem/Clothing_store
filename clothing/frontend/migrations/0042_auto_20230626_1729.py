# Generated by Django 3.2.10 on 2023-06-26 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0041_auto_20230626_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='Description'),
        ),
        migrations.AddField(
            model_name='product',
            name='material',
            field=models.CharField(default='Coton 100%', max_length=50),
        ),
    ]
