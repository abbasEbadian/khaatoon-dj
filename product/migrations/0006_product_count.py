# Generated by Django 4.0.4 on 2022-05-05 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_city_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='count',
            field=models.IntegerField(default=1, verbose_name='تعداد موجود '),
        ),
    ]
