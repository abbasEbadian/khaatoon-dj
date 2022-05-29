# Generated by Django 4.0.4 on 2022-05-24 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_alter_discount_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderline',
            name='count',
            field=models.IntegerField(default=1, verbose_name='تعداد'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='discount',
            name='uid',
            field=models.CharField(default='9QGX5IPKED', max_length=10, verbose_name='کد'),
        ),
    ]