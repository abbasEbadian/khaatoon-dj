# Generated by Django 4.0.4 on 2022-05-13 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attribute', '0002_alter_attribute_options_alter_attributevalue_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattribute',
            name='count',
            field=models.PositiveIntegerField(default=1, verbose_name='موجودی'),
        ),
    ]
