# Generated by Django 4.0.4 on 2022-05-28 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_alter_discount_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='uid',
            field=models.CharField(default='8EEACZVSGY', max_length=10, verbose_name='کد'),
        ),
    ]
