# Generated by Django 4.0.4 on 2022-05-06 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='instagram_address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='آدرس اینستاگرام'),
        ),
        migrations.AlterField(
            model_name='market',
            name='telegram_address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='آدرس تلگرام'),
        ),
        migrations.AlterField(
            model_name='market',
            name='website_address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='آدرس وبسایت'),
        ),
    ]
