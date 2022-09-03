# Generated by Django 4.0.1 on 2022-09-03 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_market_national_code_alter_market_about_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='type',
            field=models.CharField(choices=[('Hagigi', 'حقیقی'), ('Hogugi', 'حقوقی')], default='Hogugi', max_length=10),
            preserve_default=False,
        ),
    ]