# Generated by Django 4.0.4 on 2022-05-04 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rate',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=2, verbose_name='میانگین امتیاز'),
        ),
    ]
