# Generated by Django 4.1 on 2022-09-15 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0029_alter_discount_uid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discount",
            name="uid",
            field=models.CharField(
                default="B0VHGB4506", max_length=10, verbose_name="کد"
            ),
        ),
    ]
