# Generated by Django 4.0.4 on 2022-05-24 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_alter_discount_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='uid',
            field=models.CharField(default='DK84F3NJWY', max_length=10, verbose_name='کد'),
        ),
    ]