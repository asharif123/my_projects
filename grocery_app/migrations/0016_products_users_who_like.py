# Generated by Django 2.2 on 2020-08-11 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_app', '0015_delete_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='users_who_like',
            field=models.ManyToManyField(related_name='liked_products', to='grocery_app.Users'),
        ),
    ]
