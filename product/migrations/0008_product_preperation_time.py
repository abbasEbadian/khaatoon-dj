# Generated by Django 4.0.4 on 2022-05-13 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_product_market_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='preperation_time',
            field=models.PositiveIntegerField(default=1, help_text='روز کاری مورد نیاز برای آماده سازی و ارسال', verbose_name='زمان آماده سازی'),
        ),
    ]
