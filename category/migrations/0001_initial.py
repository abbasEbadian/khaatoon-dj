# Generated by Django 4.0.4 on 2022-05-04 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='انگلیسی', max_length=50, verbose_name='نام')),
                ('persian_name', models.CharField(help_text='فارسی', max_length=80, verbose_name='نام')),
                ('slug_name', models.CharField(blank=True, help_text='خودکار پر میشود', max_length=50, verbose_name='اسلاگ')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تایرخ بروزرسانی')),
                ('meta_title', models.CharField(blank=True, max_length=100, null=True, verbose_name=' تایتل')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name=' متا دسکریپشن')),
                ('meta_keywords', models.TextField(blank=True, null=True, verbose_name=' متا کیوردز')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
    ]
