# Generated by Django 4.0.4 on 2022-05-04 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('state', '0001_initial'),
        ('product', '0004_alter_product_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='city_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='state.city', verbose_name='شهر'),
        ),
    ]