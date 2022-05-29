# Generated by Django 4.0.4 on 2022-05-24 10:44

import config.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='websiteconfiguration',
            name='index_main_image_link',
            field=models.TextField(default='', verbose_name='لینک عکس کوچک دوم صفحه اصلی'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='websiteconfiguration',
            name='index_main_image',
            field=models.ImageField(upload_to=config.models.get_file_path_for_avatar, verbose_name='عکس بزرگ صفحه اصلی '),
        ),
    ]
