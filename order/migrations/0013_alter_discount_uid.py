# Generated by Django 4.0.4 on 2022-05-24 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_order_address_id_alter_discount_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='uid',
            field=models.CharField(default='GTZB7XN3HB', max_length=10, verbose_name='کد'),
        ),
    ]
