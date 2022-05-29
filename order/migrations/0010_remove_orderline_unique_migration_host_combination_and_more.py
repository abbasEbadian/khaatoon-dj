# Generated by Django 4.0.4 on 2022-05-23 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_discount_uid_alter_orderline_product_id'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='orderline',
            name='unique_migration_host_combination',
        ),
        migrations.AlterField(
            model_name='discount',
            name='uid',
            field=models.CharField(default='K5AXIE6SA7', max_length=10, verbose_name='کد'),
        ),
    ]