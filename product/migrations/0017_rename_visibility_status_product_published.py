# Generated by Django 4.0.4 on 2022-05-28 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_product_visibility_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='visibility_status',
            new_name='published',
        ),
    ]
