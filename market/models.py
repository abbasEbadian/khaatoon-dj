from django.db import models
from state.models import City, Province
from django.contrib.auth import get_user_model
User = get_user_model()


class Bank(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام بانک")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
            return   str(self.name)

    class Meta:
        verbose_name="بانک"
        verbose_name_plural="بانک ها"

class ShippingMethods(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام روش")
    description = models.TextField(verbose_name="توضیحات اختیاری")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
            return   str(self.name)

    class Meta:
        verbose_name="روش ارسال"
        verbose_name_plural="روش های ارسال"


class BusinessType(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام کسب و کار")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
            return   str(self.name)

    class Meta:
        verbose_name="نوع کسب و کار"
        verbose_name_plural="انواع کسب و کار"


def get_cover_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/markets/%s-cover.%s" % (instance.id, ext)
    return  filename

def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/markets/%s-image.%s" % (instance.id, ext)
    return  filename

def get_document_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/markets/%s-document.%s" % (instance.id, ext)
    return  filename

STATUS_CHOICES = [
    ['authenticated', 'احراز هویت شده'],
    ['pending', 'در حال بررسی مدارک'],
    ['starter', 'در حال تکمیل مدارک'],
    ['rejected', 'رد شده'],
]
class Market(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام فروشگاه")
    message = models.TextField(verbose_name="متن پیام غرفه دار",  null=True, blank=True)
    username = models.CharField(max_length=255, verbose_name="آدرس فروشگاه", unique=True, help_text="مسیر دسترسی به فروشگاه شما در مجموعه خاتون زیبا که آدرس مستقیم ورود به فروشگاه شما خواهد بود.", null=True, blank=True)
    about = models.TextField(verbose_name="درباره فروشگاه",  null=True, blank=True)
    address = models.TextField(verbose_name="آدرس فروشگاه",  null=True, blank=True)
    telegram_address = models.CharField(max_length=255, verbose_name="آدرس تلگرام", blank=True, null=True)
    instagram_address = models.CharField(max_length=255, verbose_name="آدرس اینستاگرام", blank=True, null=True)
    website_address = models.CharField(max_length=255, verbose_name="آدرس وبسایت", blank=True, null=True)
    mobile = models.CharField(max_length=255, verbose_name="شماره همراه",  null=True, blank=True)
    phone = models.CharField(max_length=255, verbose_name="تلفن ثابت", null=True, blank=True)

    shaba = models.CharField(max_length=255, verbose_name="شماره شبا", null=True, blank=True)
    card_number = models.CharField(max_length=16, verbose_name="شماره کارت", null=True, blank=True)
    national_code = models.CharField(max_length=10, verbose_name="کد ملی", null=True, blank=True)

    bank = models.ForeignKey(Bank,  on_delete=models.CASCADE, verbose_name="بانک", null=True, blank=True)
    user = models.OneToOneField(User, verbose_name="کاربر", on_delete=models.CASCADE)
    business_type = models.ForeignKey(BusinessType, on_delete=models.SET_NULL, null=True, verbose_name="نوع کسب و کار", )
    province_id = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, verbose_name="استان", )
    city_id = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="شهر", )

    cover = models.ImageField(verbose_name="تصویر کاور", upload_to=get_cover_path, blank=True, null=True)
    image = models.ImageField(verbose_name="تصویر شاخص", upload_to=get_image_path, blank=True, null=True)
    document = models.ImageField(verbose_name="تصویر مدارک", upload_to=get_document_path, blank=True, null=True)

    status = models.CharField(verbose_name="وضعیت غرفه", max_length=32, choices = STATUS_CHOICES, )
    status_message = models.TextField(verbose_name="پیام وضعیت غرفه", blank=True, help_text="در صورتی که برای مثال نواقصی در مدارک موجود بود از این طریق می توانید کاربر را مطلع سازید." )
    
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return   str(self.name) + (self.mobile and (" ( " + self.mobile + " )" ) or "")

    class Meta:
        verbose_name="غرفه"
        verbose_name_plural="غرفه ها"   
    
    def get_orders(self):
        return list(set([x.sub_order_id for x in self.orderline_set.iterator() if x.sub_order_id]))