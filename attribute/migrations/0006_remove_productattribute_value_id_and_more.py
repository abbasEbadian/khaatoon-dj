# Generated by Django 4.0.4 on 2022-05-15 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attribute', '0005_productattribute_product_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='value_id',
        ),
        migrations.AddField(
            model_name='productattribute',
            name='value_ids',
            field=models.ManyToManyField(null=True, to='attribute.attributevalue', verbose_name='مقادیر مشخصه'),
        ),
    ]