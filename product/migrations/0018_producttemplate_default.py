# Generated by Django 4.0.4 on 2022-05-28 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_rename_visibility_status_product_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttemplate',
            name='default',
            field=models.BooleanField(default=False, help_text='در صورتی که انتخاب شوندگی نداشته باشد', verbose_name='قالب اصلی'),
        ),
    ]
