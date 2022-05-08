# Generated by Django 4.0.4 on 2022-05-04 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0002_category_parent_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='نام محصول')),
                ('rate', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='میانگین امتیاز')),
                ('sales_amount', models.IntegerField(default=0, help_text='اتوماتیک', verbose_name='مجموع فروش')),
                ('sales_count', models.IntegerField(default=0, help_text='اتوماتیک', verbose_name='تعداد فروش')),
                ('price', models.DecimalField(blank=True, decimal_places=0, help_text='اتوماتیک', max_digits=9, null=True, verbose_name='قیمت به تومان')),
                ('active', models.BooleanField(default=True, verbose_name='نمایش در وبسایت')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('meta_title', models.CharField(blank=True, max_length=100, null=True, verbose_name=' تایتل')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name=' متا دسکریپشن')),
                ('meta_keywords', models.TextField(blank=True, null=True, verbose_name=' متا کیوردز')),
                ('meta_canonical', models.TextField(blank=True, null=True, verbose_name=' کنونیکال')),
                ('image_alt', models.CharField(blank=True, max_length=100, null=True, verbose_name='alt تصویر')),
                ('album', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='product.imagealbum')),
                ('category_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='category.category', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='images/')),
                ('default', models.BooleanField(default=False)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.imagealbum')),
            ],
        ),
    ]
