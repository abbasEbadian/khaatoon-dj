# Generated by Django 4.0.4 on 2022-05-24 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_alter_discount_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='uid',
            field=models.CharField(default='ILT1699S6J', max_length=10, verbose_name='کد'),
        ),
    ]
