# Generated by Django 4.0.4 on 2022-05-28 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0021_alter_discount_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='uid',
            field=models.CharField(default='WL6MQNAAPA', max_length=10, verbose_name='کد'),
        ),
    ]