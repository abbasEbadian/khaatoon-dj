# Generated by Django 4.0.4 on 2022-05-04 18:00

from django.db import migrations, models
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='album',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=product.models.get_file_path_for_image, verbose_name='َتصویر شاخص'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to=product.models.get_file_path_for_image, verbose_name='َتصویر 1'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to=product.models.get_file_path_for_image, verbose_name='َتصویر 2'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_3',
            field=models.ImageField(blank=True, null=True, upload_to=product.models.get_file_path_for_image, verbose_name='َتصویر 3'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_4',
            field=models.ImageField(blank=True, null=True, upload_to=product.models.get_file_path_for_image, verbose_name='َتصویر 4'),
        ),
    ]
