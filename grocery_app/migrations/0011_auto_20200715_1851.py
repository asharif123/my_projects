# Generated by Django 2.2 on 2020-07-16 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_app', '0010_products_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(default='chicken.JPG', upload_to=''),
        ),
    ]